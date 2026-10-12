"""Full HTTP workflow and server-enforced permissions (not button-only checks)."""

from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, override_settings
from django.urls import reverse
from django.utils import timezone

from tickets.constants import Role, Status
from tickets.models import Ticket, TicketComment
from tickets import services

from .helpers import FoundationCase, TEST_PASSWORD


class WorkflowViewTests(FoundationCase):
    def url(self, name, ticket=None):
        return reverse(f"tickets:{name}", args=[ticket.pk] if ticket else None)

    def data(self, **changes):
        values = dict(title="Email unavailable", description="Cannot send invoices.",
                      category=self.category.pk, department=self.department.pk, priority="high")
        values.update(changes)
        return values

    def test_anonymous_requests_redirect_to_login_including_mutations(self):
        ticket = self.make_ticket()
        for name in ("dashboard", "ticket_list", "ticket_create", "ticket_detail", "ticket_update", "ticket_cancel",
                     "ticket_assign", "ticket_start", "ticket_resolve", "ticket_comment"):
            target = None if name in ("dashboard", "ticket_list", "ticket_create") else ticket
            for method in ("get", "post"):
                response = getattr(self.client, method)(self.url(name, target))
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login") + "?next="))
        self.assertEqual(Ticket.objects.count(), 1)

    def test_login_bad_credentials_inactive_user_and_safe_next(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, '<label for="id_username">')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        response = self.client.post(reverse("login"), {"username": self.employee.username, "password": "incorrect"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        inactive = self.make_user("inactive-login", Role.EMPLOYEE, is_active=False)
        response = self.client.post(reverse("login"), {"username": inactive.username, "password": TEST_PASSWORD})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(reverse("login"), {"username": self.employee.username, "password": TEST_PASSWORD,
                                                     "next": "https://untrusted.example/"})
        self.assertRedirects(response, self.url("dashboard"))

    def test_logout_is_post_only_and_destroys_authenticated_session(self):
        self.client.force_login(self.employee)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(self.client.get(self.url("dashboard")).status_code, 302)

    def test_csrf_required_for_login_logout_and_every_mutation(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("login"), {"username": self.employee.username, "password": TEST_PASSWORD})
        self.assertContains(response, "Refresh the page", status_code=403)
        client.get(reverse("login"))
        token = client.cookies["csrftoken"].value
        response = client.post(reverse("login"), {"username": self.employee.username, "password": TEST_PASSWORD,
                                                  "csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 302)
        client.force_login(self.itadmin)
        ticket = self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        for name in ("ticket_create", "ticket_update", "ticket_cancel", "ticket_assign", "ticket_start", "ticket_resolve", "ticket_comment"):
            target = None if name == "ticket_create" else ticket
            self.assertEqual(client.post(self.url(name, target), self.data()).status_code, 403)
        self.assertEqual(client.post(reverse("logout")).status_code, 403)
        client.get(self.url("dashboard"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.url("ticket_comment", ticket), {"body": "Verified", "csrfmiddlewaretoken": token}).status_code, 302)
        self.assertEqual(client.post(reverse("logout"), {"csrfmiddlewaretoken": token}).status_code, 302)

    def test_invalid_role_staff_only_and_conflicting_role_fail_closed(self):
        conflicting = self.make_user("conflicting", Role.EMPLOYEE)
        User.groups.through.objects.create(user_id=conflicting.pk, group_id=self.groups[Role.TECHNICIAN].pk)
        for actor in (self.staff, conflicting):
            self.client.force_login(actor)
            for name in ("dashboard", "ticket_list", "ticket_create"):
                self.assertContains(self.client.get(self.url(name)), "exactly one application role", status_code=403)
            self.assertEqual(self.client.post(self.url("ticket_create"), self.data()).status_code, 403)
        self.assertFalse(Ticket.objects.exists())

    def test_role_scoped_lists_dashboards_and_related_detail(self):
        own_new = self.make_ticket(title="Own unassigned")
        assigned = self.make_ticket(title="Owned assigned", status=Status.ASSIGNED, assigned_to=self.technician)
        other = self.make_ticket(title="Other private issue", requester=self.other, status=Status.IN_PROGRESS,
                                 assigned_to=self.technician2)
        resolved = self.make_ticket(title="Owned resolved", status=Status.RESOLVED, assigned_to=self.technician,
                                   resolution_note="Fixed", resolved_at=timezone.now())
        cases = ((self.employee, {own_new.pk, assigned.pk, resolved.pk}, 2),
                 (self.technician, {assigned.pk, resolved.pk}, 1),
                 (self.technician2, {other.pk}, 1), (self.itadmin, {own_new.pk, assigned.pk, other.pk, resolved.pk}, 3),
                 (self.superuser, {own_new.pk, assigned.pk, other.pk, resolved.pk}, 3))
        for actor, ids, active in cases:
            self.client.force_login(actor)
            for name in ("ticket_list", "dashboard"):
                response = self.client.get(self.url(name))
                self.assertEqual(response.status_code, 200)
                self.assertEqual({t.pk for t in response.context["tickets"]}, ids)
                if name == "dashboard":
                    self.assertEqual(response.context["counts"], {"total": len(ids), "active": active, "resolved": int(resolved.pk in ids), "cancelled": 0})
                for ticket in (own_new, assigned, other, resolved):
                    if ticket.pk not in ids:
                        self.assertNotContains(response, ticket.title)
        self.client.force_login(self.employee)
        response = self.client.get(self.url("ticket_detail", assigned))
        for value in (self.category.name, self.department.name, self.employee.username, self.technician.username):
            self.assertContains(response, value)

    def test_empty_scoped_workspaces_are_useful(self):
        self.client.force_login(self.technician)
        for name in ("dashboard", "ticket_list"):
            response = self.client.get(self.url(name))
            self.assertContains(response, "No tickets yet")
            self.assertContains(response, "Tickets assigned to you")
        self.assertEqual(self.client.get(self.url("dashboard")).context["counts"]["total"], 0)

    def test_cross_user_get_and_post_on_every_object_endpoint_return_safe_404(self):
        ticket = self.make_ticket(title="Private payroll issue")
        for actor in (self.other, self.technician, self.technician2):
            self.client.force_login(actor)
            for name in ("ticket_detail", "ticket_update", "ticket_cancel"):
                for method in (("get",) if name == "ticket_detail" else ("get", "post")):
                    response = getattr(self.client, method)(self.url(name, ticket), self.data() if method == "post" else {})
                    self.assertContains(response, "This ticket is unavailable", status_code=404)
                    self.assertNotContains(response, ticket.title, status_code=404)
            for name in ("ticket_assign", "ticket_start", "ticket_resolve", "ticket_comment"):
                self.assertEqual(self.client.post(self.url(name, ticket), {"body": "attack"}).status_code, 404)
        self.assertFalse(TicketComment.objects.exists())

    def test_missing_ticket_returns_friendly_404_even_in_debug_mode(self):
        self.client.force_login(self.itadmin)
        with override_settings(DEBUG=True):
            self.assertContains(self.client.get("/tickets/999999/"), "This ticket is unavailable", status_code=404)
            self.assertEqual(self.client.post("/tickets/999999/start/").status_code, 404)

    def test_supported_http_methods_prevent_get_mutations(self):
        self.client.force_login(self.itadmin)
        ticket = self.make_ticket()
        for name in ("ticket_assign", "ticket_start", "ticket_resolve", "ticket_comment"):
            response = self.client.get(self.url(name, ticket))
            self.assertEqual(response.status_code, 405)
            self.assertEqual(response.headers["Allow"], "POST")
        for name in ("dashboard", "ticket_list", "ticket_detail"):
            self.assertEqual(self.client.post(self.url(name, ticket if name == "ticket_detail" else None)).status_code, 405)
        self.assertEqual(self.client.put(self.url("ticket_update", ticket)).status_code, 405)
        self.assertEqual(self.client.delete(self.url("ticket_cancel", ticket)).status_code, 405)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)

    def test_create_ignores_forged_protected_fields_and_redirects_with_feedback(self):
        self.client.force_login(self.employee)
        response = self.client.post(self.url("ticket_create"), self.data(requester=self.other.pk,
            assigned_to=self.technician.pk, status=Status.RESOLVED, resolution_note="Forged", resolved_at="2026-01-01", id=123))
        ticket = Ticket.objects.get()
        self.assertRedirects(response, self.url("ticket_detail", ticket), fetch_redirect_response=False)
        self.assertEqual(ticket.requester, self.employee)
        self.assertEqual(ticket.status, Status.NEW)
        self.assertIsNone(ticket.assigned_to)
        self.assertEqual(ticket.resolution_note, "")
        self.assertIsNone(ticket.resolved_at)
        self.assertContains(self.client.get(response.url), "submitted")

    def test_technician_cannot_get_or_post_create(self):
        self.client.force_login(self.technician)
        self.assertEqual(self.client.get(self.url("ticket_create")).status_code, 403)
        self.assertEqual(self.client.post(self.url("ticket_create"), self.data()).status_code, 403)
        self.assertFalse(Ticket.objects.exists())

    def test_business_form_validation_has_bound_errors_and_no_writes(self):
        self.client.force_login(self.employee)
        for changes in ({"title": " \t "}, {"description": ""}, {"title": "x" * 151}, {"priority": "urgent"},
                        {"category": "invalid"}, {"department": 99999}):
            response = self.client.post(self.url("ticket_create"), self.data(**changes))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].is_bound)
            self.assertIn(next(iter(changes)), response.context["form"].errors)
        self.assertFalse(Ticket.objects.exists())

    def test_edit_whitelists_fields_and_enforces_roles_and_state(self):
        ticket = self.make_ticket()
        self.client.force_login(self.employee)
        response = self.client.post(self.url("ticket_update", ticket), self.data(title="Updated issue", requester=self.other.pk,
            status=Status.ASSIGNED, assigned_to=self.technician.pk, resolution_note="Forged"))
        self.assertEqual(response.status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, "Updated issue")
        self.assertEqual(ticket.requester, self.employee)
        self.assertEqual(ticket.status, Status.NEW)
        self.assertIsNone(ticket.assigned_to)
        self.assertEqual(ticket.resolution_note, "")
        services.assign_ticket(self.itadmin, ticket.pk, self.technician)
        for actor in (self.employee, self.technician):
            self.client.force_login(actor)
            self.assertEqual(self.client.get(self.url("ticket_update", ticket)).status_code, 403)
            self.assertEqual(self.client.post(self.url("ticket_update", ticket), self.data()).status_code, 403)
        self.client.force_login(self.itadmin)
        self.assertEqual(self.client.post(self.url("ticket_update", ticket), self.data()).status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.ASSIGNED)
        self.assertEqual(ticket.assigned_to, self.technician)

    def test_cancel_confirmation_get_is_safe_post_retains_all_related_data(self):
        ticket = self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        comment = services.add_comment(self.employee, ticket.pk, "Keep discussion")
        self.client.force_login(self.itadmin)
        self.assertContains(self.client.get(self.url("ticket_cancel", ticket)), "cannot be edited, reopened")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.IN_PROGRESS)
        self.assertEqual(self.client.post(self.url("ticket_cancel", ticket)).status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.CANCELLED)
        self.assertEqual(ticket.assigned_to, self.technician)
        self.assertTrue(TicketComment.objects.filter(pk=comment.pk).exists())
        self.assertEqual(self.client.post(self.url("ticket_cancel", ticket)).status_code, 409)

    def test_employee_cancel_only_own_new(self):
        new = self.make_ticket()
        assigned = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        self.client.force_login(self.employee)
        self.assertEqual(self.client.get(self.url("ticket_cancel", assigned)).status_code, 403)
        self.assertEqual(self.client.post(self.url("ticket_cancel", assigned)).status_code, 403)
        self.assertEqual(self.client.post(self.url("ticket_cancel", new)).status_code, 302)

    def test_assign_forms_reject_invalid_targets_and_non_admin(self):
        ticket = self.make_ticket()
        self.client.force_login(self.employee)
        self.assertEqual(self.client.post(self.url("ticket_assign", ticket), {"assigned_to": self.technician.pk}).status_code, 403)
        self.client.force_login(self.itadmin)
        inactive = self.make_user("inactive-target", Role.TECHNICIAN, is_active=False)
        conflicting = self.make_user("conflicting-target", Role.TECHNICIAN)
        User.groups.through.objects.create(user_id=conflicting.pk, group_id=self.groups[Role.EMPLOYEE].pk)
        for target in ("", "wrong", 999999, self.employee.pk, self.superuser.pk, inactive.pk, conflicting.pk):
            response = self.client.post(self.url("ticket_assign", ticket), {"assigned_to": target})
            self.assertEqual(response.status_code, 200)
            self.assertIn("assigned_to", response.context["assignment_form"].errors)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)

    def test_reassignment_immediately_removes_old_technician_web_access(self):
        ticket = self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        self.client.force_login(self.itadmin)
        response = self.client.post(self.url("ticket_assign", ticket), {"assigned_to": self.technician2.pk, "status": Status.ASSIGNED}, follow=True)
        self.assertEqual(response.status_code, 200)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.IN_PROGRESS)
        self.client.force_login(self.technician)
        self.assertNotContains(self.client.get(self.url("ticket_list")), ticket.reference)
        self.assertEqual(self.client.get(self.url("ticket_detail", ticket)).status_code, 404)
        self.assertEqual(self.client.post(self.url("ticket_resolve", ticket), {"resolution_note": "Stale"}).status_code, 404)
        self.assertEqual(self.client.post(self.url("ticket_comment", ticket), {"body": "Stale"}).status_code, 404)
        self.client.force_login(self.technician2)
        self.assertEqual(self.client.get(self.url("ticket_detail", ticket)).status_code, 200)

    def test_start_resolution_authorization_order_and_required_note(self):
        ticket = self.make_ticket()
        self.client.force_login(self.itadmin)
        self.assertContains(self.client.post(self.url("ticket_start", ticket)), "requires a ticket in Assigned", status_code=409)
        self.client.post(self.url("ticket_assign", ticket), {"assigned_to": self.technician.pk})
        self.client.force_login(self.employee)
        for name in ("ticket_start", "ticket_resolve"):
            self.assertEqual(self.client.post(self.url(name, ticket)).status_code, 403)
        self.client.force_login(self.technician)
        self.assertEqual(self.client.post(self.url("ticket_resolve", ticket), {"resolution_note": "Too soon"}).status_code, 409)
        self.assertEqual(self.client.post(self.url("ticket_start", ticket)).status_code, 302)
        self.assertEqual(self.client.post(self.url("ticket_start", ticket)).status_code, 409)
        for note in ("", " \t "):
            response = self.client.post(self.url("ticket_resolve", ticket), {"resolution_note": note})
            self.assertEqual(response.status_code, 200)
            self.assertIn("resolution_note", response.context["resolution_form"].errors)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.IN_PROGRESS)
        self.assertIsNone(ticket.resolved_at)

    def test_admin_can_complete_web_progress_and_resolution_without_being_assignee(self):
        ticket = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        self.client.force_login(self.itadmin)
        self.assertEqual(self.client.post(self.url("ticket_start", ticket)).status_code, 302)
        self.client.force_login(self.superuser)
        self.assertEqual(self.client.post(self.url("ticket_resolve", ticket), {"resolution_note": "Verified repaired."}).status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.RESOLVED)
        self.assertEqual(ticket.assigned_to, self.technician)
        self.assertEqual(ticket.resolution_note, "Verified repaired.")

    def test_invalid_edit_retains_original_persisted_fields(self):
        ticket = self.make_ticket()
        before = Ticket.objects.values().get(pk=ticket.pk)
        self.client.force_login(self.employee)
        response = self.client.post(self.url("ticket_update", ticket), self.data(title=" \n "))
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)
        self.assertEqual(Ticket.objects.values().get(pk=ticket.pk), before)

    def test_deactivated_account_cannot_continue_existing_session(self):
        self.client.force_login(self.employee)
        self.employee.is_active = False
        self.employee.save(update_fields=["is_active"])
        self.assertEqual(self.client.get(self.url("dashboard")).status_code, 302)
        self.assertEqual(self.client.post(self.url("ticket_create"), self.data()).status_code, 302)
        self.assertFalse(Ticket.objects.exists())

    def test_comment_validation_session_author_forged_fields_and_escape(self):
        ticket = self.make_ticket()
        other = self.make_ticket(requester=self.other)
        self.client.force_login(self.employee)
        response = self.client.post(self.url("ticket_comment", ticket), {"body": " \n "})
        self.assertEqual(response.status_code, 200)
        self.assertIn("body", response.context["comment_form"].errors)
        response = self.client.post(self.url("ticket_comment", ticket), {"body": "<script>alert(1)</script>", "author": self.itadmin.pk, "ticket": other.pk})
        self.assertEqual(response.status_code, 302)
        comment = TicketComment.objects.get()
        self.assertEqual(comment.author, self.employee)
        self.assertEqual(comment.ticket, ticket)
        response = self.client.get(self.url("ticket_detail", ticket))
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_terminal_ui_and_all_admin_post_attempts_are_read_only(self):
        for state in (Status.RESOLVED, Status.CANCELLED):
            ticket = self.make_ticket(status=state, assigned_to=self.technician,
                                     resolution_note="Documented fix" if state == Status.RESOLVED else "",
                                     resolved_at=timezone.now() if state == Status.RESOLVED else None)
            before = Ticket.objects.values().get(pk=ticket.pk)
            self.client.force_login(self.itadmin)
            response = self.client.get(self.url("ticket_detail", ticket))
            self.assertContains(response, "read-only")
            for name in ("ticket_update", "ticket_cancel", "ticket_assign", "ticket_start", "ticket_resolve", "ticket_comment"):
                self.assertNotContains(response, self.url(name, ticket))
                self.assertContains(self.client.post(self.url(name, ticket), self.data()), "read-only", status_code=409)
            self.assertEqual(Ticket.objects.values().get(pk=ticket.pk), before)
        self.assertFalse(TicketComment.objects.exists())

    def test_forms_service_validation_maps_excluded_fields_to_non_field_errors(self):
        self.client.force_login(self.employee)
        from django.core.exceptions import ValidationError
        with patch("tickets.services.create_ticket", side_effect=ValidationError({"requester": "Account changed. Try again."})):
            response = self.client.post(self.url("ticket_create"), self.data())
        self.assertContains(response, "Account changed. Try again.")
        self.assertIn("__all__", response.context["form"].errors)

    def test_current_state_rechecked_after_form_validation(self):
        ticket = self.make_ticket()
        self.client.force_login(self.employee)
        original = services.update_ticket
        def change_before_save(actor, pk, values):
            services.assign_ticket(self.itadmin, pk, self.technician)
            return original(actor, pk, values)
        with patch("tickets.services.update_ticket", side_effect=change_before_save):
            response = self.client.post(self.url("ticket_update", ticket), self.data(title="Stale edit"))
        self.assertEqual(response.status_code, 403)
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, "Printer unavailable")
        self.assertEqual(ticket.status, Status.ASSIGNED)

    @override_settings(DEBUG=False)
    def test_missing_route_and_permission_error_templates(self):
        self.assertContains(self.client.get("/nonexistent/"), "This page is unavailable", status_code=404)
        self.client.force_login(self.employee)
        self.assertContains(self.client.get(self.url("ticket_create")), "Submit a ticket")
        # No custom CRUD/query/report endpoints are introduced in C.
        for path in ("/categories/", "/categories/new/"):
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_server_error_template_does_not_resolve_database_backed_user(self):
        from django.utils.functional import SimpleLazyObject
        from tickets.views import server_error
        request = RequestFactory().get("/")
        def unavailable_user():
            raise AssertionError("The error page must not resolve an unavailable database user")
        request.user = SimpleLazyObject(unavailable_user)
        with self.assertNumQueries(0):
            response = server_error(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Please try again later", response.content)

    def test_complete_persisted_employee_admin_technician_employee_journey(self):
        self.assertTrue(self.client.login(username=self.employee.username, password=TEST_PASSWORD))
        self.assertEqual(self.client.post(self.url("ticket_create"), self.data()).status_code, 302)
        ticket = Ticket.objects.get()
        self.assertEqual(self.client.post(self.url("ticket_update", ticket), self.data(description="Invoice emails fail with timeout.")).status_code, 302)
        self.assertEqual(self.client.post(self.url("ticket_comment", ticket), {"body": "Started this morning."}).status_code, 302)
        self.client.post(reverse("logout"))
        self.assertTrue(self.client.login(username=self.itadmin.username, password=TEST_PASSWORD))
        self.assertEqual(self.client.post(self.url("ticket_assign", ticket), {"assigned_to": self.technician.pk}).status_code, 302)
        self.client.post(reverse("logout"))
        self.assertTrue(self.client.login(username=self.technician.username, password=TEST_PASSWORD))
        self.assertContains(self.client.get(self.url("ticket_list")), ticket.reference)
        self.assertEqual(self.client.post(self.url("ticket_start", ticket)).status_code, 302)
        self.assertEqual(self.client.post(self.url("ticket_comment", ticket), {"body": "Checking mail settings."}).status_code, 302)
        self.assertEqual(self.client.post(self.url("ticket_resolve", ticket), {"resolution_note": "  Corrected mail configuration; test invoice delivered.  ",
            "requester": self.other.pk, "assigned_to": self.technician2.pk, "resolved_at": "2000-01-01"}).status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.RESOLVED)
        self.assertEqual(ticket.requester, self.employee)
        self.assertEqual(ticket.assigned_to, self.technician)
        self.assertTrue(timezone.is_aware(ticket.resolved_at))
        self.assertGreater(ticket.resolved_at.year, 2000)
        self.assertEqual(ticket.comments.count(), 2)
        self.client.post(reverse("logout"))
        self.assertTrue(self.client.login(username=self.employee.username, password=TEST_PASSWORD))
        response = self.client.get(self.url("ticket_detail", ticket))
        for text in ("Resolved", "Corrected mail configuration; test invoice delivered.", "Started this morning.", "Checking mail settings."):
            self.assertContains(response, text)
        self.assertEqual(self.client.get(self.url("dashboard")).context["counts"], {"total": 1, "active": 0, "resolved": 1, "cancelled": 0})
