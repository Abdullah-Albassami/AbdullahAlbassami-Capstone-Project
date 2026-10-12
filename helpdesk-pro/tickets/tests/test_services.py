"""Direct boundary tests: authorization, current state and atomic validation."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.utils import timezone

from tickets import services
from tickets.constants import Role, Status
from tickets.models import Ticket, TicketComment

from .helpers import FoundationCase


class WorkflowServiceTests(FoundationCase):
    def values(self, **changes):
        data = dict(title="  Network printer issue  ", description="  Cannot print invoices.  ",
                    category=self.category, department=self.department, priority=Ticket.Priority.HIGH)
        data.update(changes)
        return data

    def test_creation_session_requester_defaults_and_whitelist(self):
        for actor in (self.employee, self.itadmin, self.superuser):
            ticket = services.create_ticket(actor, self.values())
            self.assertEqual(ticket.requester, actor)
            self.assertEqual(ticket.status, Status.NEW)
            self.assertIsNone(ticket.assigned_to)
            self.assertIsNone(ticket.resolved_at)
            self.assertEqual(ticket.resolution_note, "")
            self.assertEqual(ticket.title, "Network printer issue")
        for values in (self.values(requester=self.other), {"title": "Incomplete"}):
            with self.assertRaises(ValidationError):
                services.create_ticket(self.employee, values)
        self.assertEqual(Ticket.objects.count(), 3)

    def test_role_and_current_account_required(self):
        for actor in (self.technician, self.staff):
            with self.assertRaises(PermissionDenied):
                services.create_ticket(actor, self.values())
        self.employee.is_active = False
        self.employee.save(update_fields=["is_active"])
        with self.assertRaises(PermissionDenied):
            services.create_ticket(self.employee, self.values())
        self.assertFalse(Ticket.objects.exists())

    def test_invalid_create_and_edit_leave_database_unchanged(self):
        with self.assertRaises(ValidationError):
            services.create_ticket(self.employee, self.values(description=" \n "))
        self.assertFalse(Ticket.objects.exists())
        ticket = self.make_ticket()
        before = Ticket.objects.values().get(pk=ticket.pk)
        with self.assertRaises(ValidationError):
            services.update_ticket(self.employee, ticket.pk, self.values(priority="urgent"))
        self.assertEqual(Ticket.objects.values().get(pk=ticket.pk), before)

    def test_edit_permissions_and_preserved_workflow_fields(self):
        ticket = self.make_ticket()
        services.update_ticket(self.employee, ticket.pk, self.values())
        ticket = services.assign_ticket(self.itadmin, ticket.pk, self.technician)
        with self.assertRaises(PermissionDenied):
            services.update_ticket(self.employee, ticket.pk, self.values())
        with self.assertRaises(PermissionDenied):
            services.update_ticket(self.technician, ticket.pk, self.values())
        ticket = services.update_ticket(self.itadmin, ticket.pk, self.values(title="Admin update"))
        self.assertEqual(ticket.status, Status.ASSIGNED)
        self.assertEqual(ticket.requester, self.employee)
        self.assertEqual(ticket.assigned_to, self.technician)
        self.assertEqual(ticket.title, "Admin update")

    def test_every_mutation_and_read_reject_out_of_scope_ids(self):
        ticket = self.make_ticket()
        calls = (
            lambda: services.get_visible_ticket(self.other, ticket.pk),
            lambda: services.update_ticket(self.other, ticket.pk, self.values()),
            lambda: services.cancel_ticket(self.other, ticket.pk),
            lambda: services.assign_ticket(self.technician, ticket.pk, self.technician),
            lambda: services.start_ticket(self.technician, ticket.pk),
            lambda: services.resolve_ticket(self.technician, ticket.pk, "Fixed"),
            lambda: services.add_comment(self.other, ticket.pk, "Forged"),
        )
        for call in calls:
            with self.subTest(call=call), self.assertRaises(Http404):
                call()
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)
        self.assertFalse(TicketComment.objects.exists())

    def test_assignment_requires_admin_and_eligible_current_account(self):
        ticket = self.make_ticket()
        with self.assertRaises(PermissionDenied):
            services.assign_ticket(self.employee, ticket.pk, self.technician)
        inactive = self.make_user("inactive-tech", Role.TECHNICIAN, is_active=False)
        for target in (None, self.employee, inactive, self.staff, self.superuser):
            with self.subTest(target=target), self.assertRaises(ValidationError):
                services.assign_ticket(self.itadmin, ticket.pk, target)
        # A fetched target becoming inactive must not pass on cached flags.
        self.technician.is_active = False
        self.technician.save(update_fields=["is_active"])
        self.technician.is_active = True
        with self.assertRaises(ValidationError):
            services.assign_ticket(self.itadmin, ticket.pk, self.technician)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)
        self.assertIsNone(ticket.assigned_to)

    def test_reassignment_preserves_each_active_assigned_state_and_revokes_old_actor(self):
        for state in (Status.ASSIGNED, Status.IN_PROGRESS):
            ticket = self.make_ticket(status=state, assigned_to=self.technician)
            saved = services.assign_ticket(self.itadmin, ticket.pk, self.technician2)
            self.assertEqual(saved.status, state)
            self.assertEqual(saved.assigned_to, self.technician2)
            with self.assertRaises(Http404):
                services.add_comment(self.technician, ticket.pk, "Stale access")
            with self.assertRaises(Http404):
                services.start_ticket(self.technician, ticket.pk)
            services.add_comment(self.technician2, ticket.pk, "Taking over")

    def test_start_and_resolve_only_legal_transitions(self):
        ticket = self.make_ticket()
        with self.assertRaises(services.WorkflowConflict):
            services.start_ticket(self.itadmin, ticket.pk)
        services.assign_ticket(self.itadmin, ticket.pk, self.technician)
        with self.assertRaises(services.WorkflowConflict):
            services.resolve_ticket(self.technician, ticket.pk, "Too soon")
        with self.assertRaises(PermissionDenied):
            services.start_ticket(self.employee, ticket.pk)
        started = services.start_ticket(self.technician, ticket.pk)
        self.assertEqual(started.status, Status.IN_PROGRESS)
        with self.assertRaises(services.WorkflowConflict):
            services.start_ticket(self.itadmin, ticket.pk)
        before = Ticket.objects.values().get(pk=ticket.pk)
        for note in ("", " \n ", None):
            with self.subTest(note=note), self.assertRaises(ValidationError):
                services.resolve_ticket(self.technician, ticket.pk, note)
            self.assertEqual(Ticket.objects.values().get(pk=ticket.pk), before)
        resolved = services.resolve_ticket(self.technician, ticket.pk, "  Replaced the faulty cable.  ")
        self.assertEqual(resolved.status, Status.RESOLVED)
        self.assertEqual(resolved.resolution_note, "Replaced the faulty cable.")
        self.assertTrue(timezone.is_aware(resolved.resolved_at))

    def test_administrator_can_start_and_resolve(self):
        ticket = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        services.start_ticket(self.itadmin, ticket.pk)
        self.assertEqual(services.resolve_ticket(self.superuser, ticket.pk, "Verified fixed").status, Status.RESOLVED)

    def test_cancellation_preserves_assignment_thread_and_ticket(self):
        ticket = self.make_ticket()
        comment = services.add_comment(self.employee, ticket.pk, "  Context  ")
        services.cancel_ticket(self.employee, ticket.pk)
        self.assertTrue(Ticket.objects.filter(pk=ticket.pk).exists())
        self.assertTrue(TicketComment.objects.filter(pk=comment.pk, body="Context").exists())
        for state in (Status.ASSIGNED, Status.IN_PROGRESS):
            ticket = self.make_ticket(status=state, assigned_to=self.technician)
            with self.assertRaises(PermissionDenied):
                services.cancel_ticket(self.employee, ticket.pk)
            with self.assertRaises(PermissionDenied):
                services.cancel_ticket(self.technician, ticket.pk)
            cancelled = services.cancel_ticket(self.itadmin, ticket.pk)
            self.assertEqual(cancelled.assigned_to, self.technician)
            self.assertEqual(cancelled.status, Status.CANCELLED)

    def test_terminal_states_block_every_mutation_including_noops(self):
        for state in (Status.RESOLVED, Status.CANCELLED):
            ticket = self.make_ticket(status=state, assigned_to=self.technician,
                resolution_note="Fixed" if state == Status.RESOLVED else "",
                resolved_at=timezone.now() if state == Status.RESOLVED else None)
            before = Ticket.objects.values().get(pk=ticket.pk)
            for action in (
                lambda: services.update_ticket(self.itadmin, ticket.pk, self.values()),
                lambda: services.assign_ticket(self.itadmin, ticket.pk, self.technician),
                lambda: services.start_ticket(self.itadmin, ticket.pk),
                lambda: services.resolve_ticket(self.itadmin, ticket.pk, "Again"),
                lambda: services.cancel_ticket(self.itadmin, ticket.pk),
                lambda: services.add_comment(self.itadmin, ticket.pk, "Late"),
            ):
                with self.subTest(state=state, action=action), self.assertRaises(services.WorkflowConflict):
                    action()
            self.assertEqual(Ticket.objects.values().get(pk=ticket.pk), before)
        self.assertFalse(TicketComment.objects.exists())

    def test_comment_author_is_actor_and_ticket_timestamp_is_unchanged(self):
        ticket = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        timestamp = ticket.updated_at
        for actor in (self.employee, self.technician, self.itadmin):
            comment = services.add_comment(actor, ticket.pk, "  Helpful context  ")
            self.assertEqual(comment.author, actor)
            self.assertEqual(comment.body, "Helpful context")
        with self.assertRaises(ValidationError):
            services.add_comment(self.employee, ticket.pk, " \t ")
        ticket.refresh_from_db()
        self.assertEqual(ticket.updated_at, timestamp)
        self.assertEqual(ticket.comments.count(), 3)
