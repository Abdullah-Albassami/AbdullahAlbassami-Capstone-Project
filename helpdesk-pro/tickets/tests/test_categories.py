from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models.deletion import ProtectedError
from django.test import Client
from django.urls import reverse

from tickets import services
from tickets.constants import Status
from tickets.models import Category

from .helpers import FoundationCase


class CategoryTests(FoundationCase):
    def url(self, name, category=None):
        return reverse(f"tickets:category_{name}", args=[category.pk] if category else None)

    def test_complete_admin_category_crud_and_related_ticket_link(self):
        self.client.force_login(self.itadmin)
        response = self.client.post(self.url("create"), {"name": "  Printing  ", "description": "  Print devices  ", "id": self.category.pk})
        category = Category.objects.get(name="Printing")
        self.assertNotEqual(category.pk, self.category.pk)
        self.assertEqual(category.description, "Print devices")
        self.assertRedirects(response, self.url("detail", category))
        response = self.client.get(self.url("list"))
        self.assertContains(response, "Printing")
        self.assertContains(response, "Print devices")
        self.assertContains(response, self.url("update", category))
        self.assertContains(response, self.url("delete", category))
        self.assertContains(self.client.get(self.url("detail", category)), f"?category={category.pk}")
        self.assertContains(self.client.get(self.url("update", category)), "Print devices")
        self.assertEqual(self.client.post(self.url("update", category), {"name": "  Printers  ", "description": "<script>notes</script>"}).status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.name, "Printers")
        self.assertContains(self.client.get(self.url("detail", category)), "&lt;script&gt;notes&lt;/script&gt;")
        self.assertContains(self.client.get(self.url("delete", category)), "permanently removes")
        self.assertTrue(Category.objects.filter(pk=category.pk).exists())
        self.assertRedirects(self.client.post(self.url("delete", category)), self.url("list"))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

    def test_category_permissions_on_every_get_and_forged_post(self):
        for actor in (self.employee, self.technician, self.staff):
            self.client.force_login(actor)
            for name in ("list", "create", "detail", "update", "delete"):
                target = self.category if name in ("detail", "update", "delete") else None
                self.assertEqual(self.client.get(self.url(name, target)).status_code, 403)
                if name in ("create", "update", "delete"):
                    self.assertEqual(self.client.post(self.url(name, target), {"name": "Forged", "description": ""}).status_code, 403)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Test category")
        self.assertEqual(Category.objects.count(), 1)

    def test_anonymous_category_requests_redirect(self):
        for name in ("list", "create", "detail", "update", "delete"):
            target = self.category if name in ("detail", "update", "delete") else None
            for method in ("get", "post"):
                response = getattr(self.client, method)(self.url(name, target))
                self.assertEqual(response.status_code, 302)
                self.assertIn("/accounts/login/?next=", response.url)

    def test_category_validation_missing_whitespace_length_and_duplicate(self):
        self.client.force_login(self.itadmin)
        for name in ("", " \t ", "x" * 101, "Test category", " Test category "):
            response = self.client.post(self.url("create"), {"name": name, "description": ""})
            self.assertEqual(response.status_code, 200)
            self.assertIn("name", response.context["form"].errors)
        other = Category.objects.create(name="Other")
        response = self.client.post(self.url("update", other), {"name": "Test category", "description": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        other.refresh_from_db()
        self.assertEqual(other.name, "Other")
        self.assertEqual(Category.objects.count(), 2)

    def test_delete_protects_active_and_terminal_references(self):
        self.client.force_login(self.itadmin)
        active = self.make_ticket()
        cancelled = self.make_ticket(status=Status.CANCELLED)
        response = self.client.post(self.url("delete", self.category))
        self.assertContains(response, "used by existing tickets and cannot be deleted")
        self.assertEqual(response.context["ticket_count"], 2)
        active.delete()  # privileged test maintenance leaves only a terminal reference
        response = self.client.post(self.url("delete", self.category))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["ticket_count"], 1)
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())
        self.assertTrue(cancelled.__class__.objects.filter(pk=cancelled.pk).exists())

    def test_methods_missing_records_and_superuser_override(self):
        self.client.force_login(self.superuser)
        self.assertEqual(self.client.get(self.url("list")).status_code, 200)
        self.assertEqual(self.client.post(self.url("list")).status_code, 405)
        self.assertEqual(self.client.post(self.url("detail", self.category)).status_code, 405)
        self.assertEqual(self.client.delete(self.url("delete", self.category)).status_code, 405)
        for path in ("/categories/999999/", "/categories/999999/edit/", "/categories/999999/delete/"):
            self.assertContains(self.client.get(path), "This category is unavailable", status_code=404)

    def test_category_services_authorize_validate_and_protect(self):
        data = {"name": "  Accessories  ", "description": "  Optional equipment  "}
        for operation in (lambda: services.create_category(self.employee, data),
                          lambda: services.update_category(self.employee, self.category.pk, data),
                          lambda: services.delete_category(self.employee, self.category.pk)):
            with self.assertRaises(PermissionDenied):
                operation()
        category = services.create_category(self.itadmin, data)
        self.assertEqual((category.name, category.description), ("Accessories", "Optional equipment"))
        with self.assertRaises(ValidationError):
            services.create_category(self.itadmin, dict(data, id=500))
        with self.assertRaises(ValidationError):
            services.update_category(self.itadmin, category.pk, {"name": "Test category", "description": ""})
        category.refresh_from_db()
        self.assertEqual(category.name, "Accessories")
        self.make_ticket(category=category)
        with self.assertRaises(ProtectedError):
            services.delete_category(self.itadmin, category.pk)
        self.assertTrue(Category.objects.filter(pk=category.pk).exists())

    def test_category_mutations_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.itadmin)
        for name in ("create", "update", "delete"):
            target = None if name == "create" else self.category
            self.assertEqual(client.post(self.url(name, target), {"name": "No token"}).status_code, 403)
        client.get(self.url("create"))
        token = client.cookies["csrftoken"].value
        response = client.post(self.url("create"), {"name": "Verified", "description": "", "csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="Verified").exists())

    def test_empty_category_list_and_description(self):
        self.client.force_login(self.itadmin)
        self.assertContains(self.client.get(self.url("detail", self.category)), "No description provided")
        self.category.delete()
        self.assertContains(self.client.get(self.url("list")), "No categories yet")
