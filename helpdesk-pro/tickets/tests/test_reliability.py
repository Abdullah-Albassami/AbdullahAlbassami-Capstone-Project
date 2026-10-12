"""Audit regressions for privacy, invalid requests and accessible form output."""

from unittest.mock import patch

from django.test import Client, override_settings
from django.urls import reverse
from django.utils import timezone

from tickets import services
from tickets.constants import Role, Status
from tickets.models import Ticket, TicketComment
from tickets.tests.helpers import FoundationCase, TEST_PASSWORD


class ReliabilityTests(FoundationCase):
    def test_logout_clears_unread_messages_before_another_account_signs_in(self):
        ticket = self.make_ticket(requester=self.other)
        self.client.force_login(self.itadmin)
        self.client.post(reverse("tickets:ticket_assign", args=[ticket.pk]), {"assigned_to": self.technician.pk})
        # Interrupt the success redirect, then sign out. Cookie-backed messages
        # must not reveal this out-of-scope ticket to the next account/login page.
        self.client.post(reverse("logout"))
        response = self.client.get(reverse("login"))
        self.assertNotContains(response, ticket.reference)
        self.assertTrue(self.client.login(username=self.employee.username, password=TEST_PASSWORD))
        self.assertNotContains(self.client.get(reverse("tickets:dashboard")), ticket.reference)

    def test_unsupported_application_method_has_helpful_405_and_allow_header(self):
        self.client.force_login(self.itadmin)
        ticket = self.make_ticket()
        for path in (reverse("tickets:ticket_start", args=[ticket.pk]), reverse("logout")):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 405)
            self.assertContains(response, "Use the page controls", status_code=405)
            self.assertIn("POST", response.headers["Allow"])
        self.assertIn("_auth_user_id", self.client.session)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)

    def test_assignment_labels_show_name_username_fallback_and_keep_user_ids(self):
        self.technician.first_name, self.technician.last_name = "Lina", "Demo"
        self.technician.save(update_fields=["first_name", "last_name"])
        self.client.force_login(self.itadmin)
        ticket = self.make_ticket()
        response = self.client.get(reverse("tickets:ticket_detail", args=[ticket.pk]))
        self.assertContains(response, f'<option value="{self.technician.pk}">Lina Demo (support)</option>', html=True)
        self.assertContains(response, f'<option value="{self.technician2.pk}">support2</option>', html=True)
        response = self.client.post(reverse("tickets:ticket_assign", args=[ticket.pk]), {"assigned_to": self.technician.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.get(pk=ticket.pk).assigned_to_id, self.technician.pk)

    def test_ticket_queue_displays_requester_with_readable_name(self):
        self.employee.first_name, self.employee.last_name = "Nora", "Demo"
        self.employee.save(update_fields=["first_name", "last_name"])
        self.make_ticket()
        self.client.force_login(self.itadmin)
        response = self.client.get(reverse("tickets:ticket_list"))
        self.assertContains(response, '<th scope="col">Requester</th>', html=True)
        self.assertContains(response, '<td>Nora Demo</td>', html=True)

    @override_settings(MESSAGE_STORAGE="django.contrib.messages.storage.session.SessionStorage")
    def test_logout_also_clears_session_backed_feedback(self):
        self.test_logout_clears_unread_messages_before_another_account_signs_in()

    def test_successful_login_account_switch_clears_previous_feedback(self):
        ticket = self.make_ticket(requester=self.other)
        self.client.force_login(self.itadmin)
        self.client.post(reverse("tickets:ticket_assign", args=[ticket.pk]), {"assigned_to": self.technician.pk})
        response = self.client.post(reverse("login"), {"username": self.employee.username, "password": TEST_PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(self.client.get(reverse("tickets:dashboard")), ticket.reference)

    def test_admin_logout_clears_pending_admin_feedback(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse("admin:tickets_category_add"), {"name": "Pending admin category", "description": ""})
        self.assertEqual(response.status_code, 302)
        self.client.post(reverse("admin:logout"))
        self.assertNotContains(self.client.get(reverse("login")), "Pending admin category")

    def test_assignment_labels_escape_names_and_exclude_ineligible_users(self):
        self.technician.first_name = "<img src=x onerror=alert(1)>"
        self.technician.save(update_fields=["first_name"])
        inactive = self.make_user("inactive-selection", Role.TECHNICIAN, is_active=False)
        ticket = self.make_ticket()
        self.client.force_login(self.itadmin)
        response = self.client.get(reverse("tickets:ticket_detail", args=[ticket.pk]))
        self.assertContains(response, "&lt;img src=x onerror=alert(1)&gt; (support)")
        self.assertNotContains(response, "<img src=x")
        choices = response.context["assignment_form"].fields["assigned_to"].queryset
        self.assertNotIn(inactive.pk, choices.values_list("pk", flat=True))
        self.assertNotIn(self.superuser.pk, choices.values_list("pk", flat=True))

    def test_assignment_rechecks_eligibility_after_valid_form_selection(self):
        ticket = self.make_ticket()
        self.client.force_login(self.itadmin)
        original = services.assign_ticket
        def deactivate_before_assign(actor, pk, technician):
            technician.is_active = False
            technician.save(update_fields=["is_active"])
            return original(actor, pk, technician)
        with patch("tickets.services.assign_ticket", side_effect=deactivate_before_assign):
            response = self.client.post(reverse("tickets:ticket_assign", args=[ticket.pk]), {"assigned_to": self.technician.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn("assigned_to", response.context["assignment_form"].errors)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)
        self.assertIsNone(ticket.assigned_to_id)

    def test_forged_role_and_report_parameters_cannot_change_scope(self):
        own = self.make_ticket()
        hidden = self.make_ticket(requester=self.other, title="Private other issue", assigned_to=self.technician2, status=Status.ASSIGNED)
        self.client.force_login(self.employee)
        response = self.client.get(reverse("tickets:dashboard"), {"role": "IT Admin", "report": "workload", "requester": self.other.pk})
        self.assertEqual(response.context["counts"]["total"], 1)
        self.assertNotIn("technicians", response.context)
        self.assertNotContains(response, hidden.title)
        response = self.client.get(reverse("tickets:ticket_list"), {"requester": self.other.pk, "assigned_to": self.technician2.pk, "role": "IT Admin"})
        self.assertEqual(list(response.context["tickets"]), [own])
        self.assertNotContains(response, hidden.title)

    def test_existing_session_loses_application_access_after_role_removal(self):
        ticket = self.make_ticket()
        self.client.force_login(self.employee)
        self.employee.groups.clear()
        for method, path in (("get", reverse("tickets:ticket_detail", args=[ticket.pk])),
                             ("post", reverse("tickets:ticket_cancel", args=[ticket.pk]))):
            self.assertEqual(getattr(self.client, method)(path).status_code, 403)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)

    def test_all_visible_roles_have_terminal_readonly_controls_and_reject_forged_changes(self):
        for state in (Status.RESOLVED, Status.CANCELLED):
            ticket = self.make_ticket(status=state, assigned_to=self.technician,
                resolution_note="Fixed" if state == Status.RESOLVED else "", resolved_at=timezone.now() if state == Status.RESOLVED else None)
            before = Ticket.objects.values().get(pk=ticket.pk)
            for actor in (self.employee, self.technician, self.itadmin):
                self.client.force_login(actor)
                response = self.client.get(reverse("tickets:ticket_detail", args=[ticket.pk]))
                self.assertContains(response, "read-only")
                for action in ("assign", "start", "resolve", "comment", "update", "cancel"):
                    path = reverse("tickets:ticket_" + action, args=[ticket.pk])
                    self.assertNotContains(response, path)
                    attempt = self.client.post(path, {"body": "Late comment", "status": "new", "assigned_to": self.technician2.pk})
                    self.assertIn(attempt.status_code, (403, 409))
            self.assertEqual(Ticket.objects.values().get(pk=ticket.pk), before)
        self.assertFalse(TicketComment.objects.exists())

    def test_huge_category_ids_null_search_and_query_payloads_fail_safely(self):
        self.make_ticket(priority="high")
        self.client.force_login(self.employee)
        for data in ({"category": "9" * 5000}, {"q": "bad\x00text"}, {"category": "-1"},
                     {"order": "priority; DROP TABLE tickets_ticket"}):
            response = self.client.get(reverse("tickets:ticket_list"), dict(data, priority="high"))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["filter_form"].errors)
            self.assertEqual(response.context["page_obj"].paginator.count, 1)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_csrf_token_rotates_at_login_and_old_token_cannot_mutate(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("login"))
        old_token = client.cookies["csrftoken"].value
        response = client.post(reverse("login"), {"username": self.employee.username, "password": TEST_PASSWORD,
                                                  "csrfmiddlewaretoken": old_token})
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(client.cookies["csrftoken"].value, old_token)
        self.assertEqual(client.post(reverse("logout"), {"csrfmiddlewaretoken": old_token}).status_code, 403)
        self.assertIn("_auth_user_id", client.session)

    def test_logout_next_redirect_does_not_allow_external_destination(self):
        self.client.force_login(self.employee)
        response = self.client.post(reverse("logout"), {"next": "https://untrusted.example/"})
        self.assertRedirects(response, reverse("login"))

    def test_authenticated_ticket_report_and_category_pages_prevent_response_storage(self):
        ticket = self.make_ticket()
        self.client.force_login(self.itadmin)
        for path in (reverse("tickets:dashboard"), reverse("tickets:ticket_list"),
                     reverse("tickets:ticket_detail", args=[ticket.pk]), reverse("tickets:category_list")):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            directives = response.headers.get("Cache-Control", "")
            self.assertIn("no-store", directives)
            self.assertIn("private", directives)
