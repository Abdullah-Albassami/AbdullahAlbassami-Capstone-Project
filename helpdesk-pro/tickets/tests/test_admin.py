from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from django.test import RequestFactory

from tickets.admin_forms import GuardedGroupForm, GuardedUserChangeForm, GuardedUserCreationForm
from tickets.constants import Role, Status
from tickets.models import Department, Ticket, TicketComment

from .helpers import FoundationCase, TEST_PASSWORD


class AdminTests(FoundationCase):
    def test_ticket_and_comment_readonly_even_for_superuser_forged_posts(self):
        ticket = self.make_ticket()
        comment = TicketComment.objects.create(ticket=ticket, author=self.employee, body="Details")
        self.client.force_login(self.superuser)
        for model, obj in ((Ticket, ticket), (TicketComment, comment)):
            app, name = model._meta.app_label, model._meta.model_name
            with self.subTest(model=name):
                change = reverse(f"admin:{app}_{name}_change", args=[obj.pk])
                response = self.client.get(change)
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.context["has_change_permission"])
                self.assertEqual(self.client.post(change, {"title": "Changed", "body": "Changed"}).status_code, 403)
                self.assertEqual(self.client.get(reverse(f"admin:{app}_{name}_add")).status_code, 403)
                self.assertEqual(self.client.post(reverse(f"admin:{app}_{name}_delete", args=[obj.pk]), {"post": "yes"}).status_code, 403)
                self.assertEqual(admin.site._registry[model].get_actions(response.wsgi_request), {})
        ticket.refresh_from_db()
        comment.refresh_from_db()
        self.assertEqual(ticket.title, "Printer unavailable")
        self.assertEqual(comment.body, "Details")

    def test_it_admin_department_setup_but_no_account_or_ticket_admin(self):
        self.client.force_login(self.itadmin)
        self.assertEqual(self.client.get(reverse("admin:tickets_department_changelist")).status_code, 200)
        response = self.client.post(reverse("admin:tickets_department_add"), {"name": "New department", "_save": "Save"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Department.objects.filter(name="New department").exists())
        for route in ("admin:auth_user_changelist", "admin:auth_group_changelist", "admin:tickets_ticket_changelist"):
            self.assertEqual(self.client.get(reverse(route)).status_code, 403)

    def test_staff_without_it_admin_role_cannot_use_department_even_with_permission(self):
        self.staff.user_permissions.add(Permission.objects.get(codename="view_department", content_type__app_label="tickets"))
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(reverse("admin:tickets_department_changelist")).status_code, 403)

    def test_department_protected_deletion_has_friendly_admin_page(self):
        self.make_ticket()
        self.client.force_login(self.itadmin)
        url = reverse("admin:tickets_department_delete", args=[self.department.pk])
        response = self.client.post(url, {"post": "yes"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["protected"])
        self.assertTrue(Department.objects.filter(pk=self.department.pk).exists())

    def test_user_creation_form_requires_exactly_one_role_and_hashes_password(self):
        base = {"username": "created", "password1": TEST_PASSWORD, "password2": TEST_PASSWORD,
                "usable_password": "true", "is_active": True}
        for groups in ([], [self.groups[Role.EMPLOYEE].pk, self.groups[Role.TECHNICIAN].pk]):
            form = GuardedUserCreationForm(data={**base, "groups": groups})
            self.assertFalse(form.is_valid())
            self.assertTrue(form.non_field_errors())
        form = GuardedUserCreationForm(data={**base, "groups": [self.groups[Role.IT_ADMIN].pk]})
        self.assertTrue(form.is_valid(), form.errors.as_text())
        user = form.save()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(TEST_PASSWORD))
        self.assertNotEqual(user.password, TEST_PASSWORD)
        self.assertEqual(list(user.groups.values_list("name", flat=True)), [Role.IT_ADMIN])

    def test_user_creation_admin_endpoint_integrates_group_and_password_fields(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("admin:auth_user_add"), {
            "username": "provisioned", "password1": TEST_PASSWORD, "password2": TEST_PASSWORD,
            "usable_password": "true", "groups": [self.groups[Role.TECHNICIAN].pk], "is_active": "on", "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="provisioned")
        self.assertEqual(list(user.groups.values_list("name", flat=True)), [Role.TECHNICIAN])
        self.assertTrue(user.check_password(TEST_PASSWORD))

    def test_user_change_form_blocks_stranding_and_empty_roles(self):
        self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        base = {"username": self.technician.username, "date_joined": self.technician.date_joined.isoformat()}
        for role_ids, active in (([], True), ([self.groups[Role.EMPLOYEE].pk], True), ([self.groups[Role.TECHNICIAN].pk], False)):
            self.technician.refresh_from_db()
            form = GuardedUserChangeForm(instance=self.technician, data={**base, "groups": role_ids, "is_active": active})
            self.assertFalse(form.is_valid())
            self.assertTrue(form.non_field_errors())
        self.technician.refresh_from_db()
        self.assertTrue(self.technician.is_active)

    def test_user_admin_post_stranding_returns_errors_without_mutation(self):
        self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        self.client.force_login(self.superuser)
        url = reverse("admin:auth_user_change", args=[self.technician.pk])
        response = self.client.post(url, {"username": self.technician.username, "groups": [self.groups[Role.TECHNICIAN].pk],
                                         "date_joined_0": "2026-10-01", "date_joined_1": "09:00:00", "_save": "Save"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reassign this account")
        self.technician.refresh_from_db()
        self.assertTrue(self.technician.is_active)

    def test_reserved_group_admin_forged_change_delete_and_form_masquerade(self):
        self.client.force_login(self.superuser)
        group = self.groups[Role.TECHNICIAN]
        self.assertEqual(self.client.get(reverse("admin:auth_group_change", args=[group.pk])).status_code, 200)
        self.assertEqual(self.client.post(reverse("admin:auth_group_change", args=[group.pk]), {"name": "Renamed"}).status_code, 403)
        self.assertEqual(self.client.post(reverse("admin:auth_group_delete", args=[group.pk]), {"post": "yes"}).status_code, 403)
        unrelated = Group.objects.create(name="Unrelated")
        form = GuardedGroupForm(instance=unrelated, data={"name": Role.TECHNICIAN, "permissions": []})
        self.assertFalse(form.is_valid())

    def test_superuser_permissions_use_persisted_flags(self):
        request = RequestFactory().get("/admin/")
        self.employee.is_superuser = True
        self.employee.is_staff = True
        request.user = self.employee
        self.assertFalse(admin.site._registry[User].has_change_permission(request))
        self.assertFalse(admin.site._registry[Ticket].has_view_permission(request))

    def test_superuser_demotion_with_multiple_roles_is_integrated(self):
        subject = User.objects.create_superuser("secondary", password=TEST_PASSWORD)
        subject.groups.add(self.groups[Role.EMPLOYEE], self.groups[Role.TECHNICIAN])
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("admin:auth_user_change", args=[subject.pk]), {
            "username": subject.username, "groups": [self.groups[Role.EMPLOYEE].pk],
            "is_active": "on", "is_staff": "on", "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        subject.refresh_from_db()
        self.assertFalse(subject.is_superuser)
        self.assertEqual(list(subject.groups.values_list("name", flat=True)), [Role.EMPLOYEE])
