from django import forms
from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, models, transaction
from django.db.models.deletion import ProtectedError
from django.utils import timezone

from tickets.constants import Status
from tickets.models import Category, Department, Ticket, TicketComment

from .helpers import FoundationCase


class ModelTests(FoundationCase):
    def test_defaults_reference_relationships_and_ordering(self):
        ticket = self.make_ticket()
        newer = self.make_ticket(title="Second issue")
        self.assertEqual((ticket.status, ticket.priority, ticket.assigned_to, ticket.resolved_at), ("new", "medium", None, None))
        self.assertEqual(ticket.reference, f"HD-{ticket.pk:05d}")
        self.assertEqual(list(self.employee.submitted_tickets.all()), [newer, ticket])
        self.assertEqual(self.category.tickets.count(), 2)
        self.assertEqual(self.department.tickets.count(), 2)
        self.assertTrue(ticket.created_at and ticket.updated_at)

    def test_required_text_trim_and_blank_rejection(self):
        ticket = self.make_ticket(title="  Printer issue  ", description="  Details  ")
        self.assertEqual((ticket.title, ticket.description), ("Printer issue", "Details"))
        for field in ("title", "description"):
            with self.subTest(field=field):
                setattr(ticket, field, " \n\t ")
                with self.assertRaises(ValidationError):
                    ticket.full_clean()
                ticket.refresh_from_db()
        for model in (Category, Department):
            instance = model(name=" \n ")
            with self.assertRaises(ValidationError):
                instance.full_clean()

    def test_lengths_uniqueness_case_sensitive_names_and_fk_validation(self):
        for model in (Category, Department):
            with self.subTest(model=model):
                with self.assertRaises(ValidationError):
                    model(name="x" * 101).full_clean()
                first = model(name=" Unique ")
                first.full_clean()
                first.save()
                with self.assertRaises(ValidationError):
                    model(name="Unique").full_clean()
                with self.assertRaises(IntegrityError), transaction.atomic():
                    model.objects.create(name="Unique")
                model.objects.create(name="unique")
        ticket = self.make_ticket()
        ticket.title = "x" * 151
        with self.assertRaises(ValidationError):
            ticket.full_clean()
        ticket.title = "Valid"
        ticket.category_id = 999999
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_null_optional_text_returns_validation_error(self):
        category = Category(name="Valid", description=None)
        with self.assertRaises(ValidationError):
            category.full_clean()
        ticket = self.make_ticket()
        ticket.resolution_note = None
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_model_rejects_invalid_choices_and_assignment_states(self):
        ticket = self.make_ticket()
        for values in (
            {"status": "unknown"}, {"priority": "urgent"},
            {"assigned_to": self.technician}, {"status": Status.ASSIGNED},
            {"status": Status.IN_PROGRESS},
            {"status": Status.ASSIGNED, "assigned_to": self.employee},
            {"status": Status.ASSIGNED, "assigned_to_id": "invalid"},
        ):
            with self.subTest(values=list(values)):
                ticket.refresh_from_db()
                for field, value in values.items():
                    setattr(ticket, field, value)
                with self.assertRaises(ValidationError):
                    ticket.full_clean()

    def test_inactive_technician_assignment_rejected(self):
        self.technician.is_active = False
        self.technician.save()
        with self.assertRaises(ValidationError):
            self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)

    def test_superuser_is_not_a_technician_target(self):
        with self.assertRaises(ValidationError):
            self.make_ticket(status=Status.ASSIGNED, assigned_to=self.superuser)

    def test_resolution_requires_assignee_note_timestamp_and_trims_note(self):
        ticket = self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        for note, timestamp in (("", None), (" \n ", timezone.now()), ("Fixed", None)):
            ticket.status = Status.RESOLVED
            ticket.resolution_note = note
            ticket.resolved_at = timestamp
            with self.assertRaises(ValidationError):
                ticket.full_clean()
        ticket.resolution_note = "  Replaced cable  "
        ticket.resolved_at = timezone.now()
        ticket.full_clean()
        ticket.save()
        self.assertEqual(ticket.resolution_note, "Replaced cable")

    def test_nonresolved_resolution_information_rejected(self):
        ticket = self.make_ticket()
        for note, timestamp in (("Fixed", None), ("", timezone.now())):
            ticket.resolution_note, ticket.resolved_at = note, timestamp
            with self.assertRaises(ValidationError):
                ticket.full_clean()

    def test_terminal_validation_and_historical_assignee(self):
        for status in (Status.RESOLVED, Status.CANCELLED):
            ticket = self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
            ticket.status = status
            if status == Status.RESOLVED:
                ticket.resolution_note, ticket.resolved_at = "Fixed", timezone.now()
            ticket.full_clean()
            ticket.save()
            ticket.title = "Forbidden edit"
            with self.assertRaises(ValidationError):
                ticket.full_clean()
        self.technician.is_active = False
        self.technician.save()
        ticket.refresh_from_db()
        ticket.full_clean()

    def test_cross_field_errors_work_with_limited_modelform(self):
        class EditForm(forms.ModelForm):
            class Meta:
                model = Ticket
                fields = ("title", "description", "category", "department", "priority")
        ticket = self.make_ticket()
        ticket.status = Status.ASSIGNED
        form = EditForm(instance=ticket, data={"title": "Valid", "description": "Valid", "category": self.category.pk,
                                             "department": self.department.pk, "priority": "medium"})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors())

    def test_comment_validation_immutability_author_scope_and_ordering(self):
        ticket = self.make_ticket()
        comment = TicketComment(ticket=ticket, author=self.employee, body="  Details  ")
        comment.full_clean()
        comment.save()
        self.assertEqual(comment.body, "Details")
        self.assertEqual(list(self.employee.ticket_comments.all()), [comment])
        for author, body in ((self.employee, " \n "), (self.other, "Not mine"), (self.technician, "Not assigned")):
            with self.assertRaises(ValidationError):
                TicketComment(ticket=ticket, author=author, body=body).full_clean()
        comment.body = "Changed"
        with self.assertRaises(ValidationError):
            comment.full_clean()
        comment.refresh_from_db()
        admin_comment = TicketComment(ticket=ticket, author=self.itadmin, body="Received")
        admin_comment.full_clean()
        admin_comment.save()
        self.assertEqual(list(ticket.comments.all()), [comment, admin_comment])
        ticket.status = Status.CANCELLED
        ticket.full_clean()
        ticket.save()
        with self.assertRaises(ValidationError):
            TicketComment(ticket=ticket, author=self.employee, body="Too late").full_clean()
        comment.full_clean()  # existing historical discussion remains valid

    def test_database_checks_even_without_full_clean(self):
        ticket = self.make_ticket()
        for values in (
            {"status": "bad"}, {"priority": "bad"},
            {"assigned_to": self.technician}, {"status": Status.ASSIGNED}, {"status": Status.IN_PROGRESS},
            {"status": Status.RESOLVED, "assigned_to": self.technician, "resolution_note": "Fixed"},
            {"status": Status.RESOLVED, "assigned_to": self.technician, "resolved_at": timezone.now()},
            {"status": Status.RESOLVED, "resolution_note": "Fixed", "resolved_at": timezone.now()},
            {"resolution_note": "Not resolved"}, {"resolved_at": timezone.now()},
        ):
            with self.subTest(fields=list(values)):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    Ticket.objects.filter(pk=ticket.pk).update(**values)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Status.NEW)

    def test_database_accepts_resolved_and_both_cancelled_assignment_options(self):
        ticket = self.make_ticket()
        Ticket.objects.filter(pk=ticket.pk).update(status=Status.RESOLVED, assigned_to=self.technician,
                                                 resolution_note="Fixed", resolved_at=timezone.now())
        for assignee in (None, self.technician):
            self.make_ticket(status=Status.CANCELLED, assigned_to=assignee)

    def test_database_foreign_key_constraint(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Ticket.objects.create(title="Invalid FK", description="Invalid reference", category_id=999999,
                                  department=self.department, requester=self.employee)
            connection.check_constraints()

    def test_protected_deletion_all_five_parent_references(self):
        ticket = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        comment = TicketComment.objects.create(ticket=ticket, author=self.itadmin, body="Received")
        for parent in (self.category, self.department, self.employee, self.technician, self.itadmin):
            with self.subTest(parent=type(parent).__name__):
                with self.assertRaises(ProtectedError):
                    parent.delete()
        self.assertTrue(TicketComment.objects.filter(pk=comment.pk).exists())

    def test_unused_category_delete_and_privileged_ticket_cascade(self):
        unused = Category.objects.create(name="Unused test category")
        unused.delete()
        ticket = self.make_ticket()
        TicketComment.objects.create(ticket=ticket, author=self.employee, body="Details")
        ticket.delete()  # privileged maintenance only; supported admin cannot do this
        self.assertFalse(TicketComment.objects.exists())

    def test_cancellation_preserves_dependencies_and_assignee(self):
        ticket = self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        comment = TicketComment.objects.create(ticket=ticket, author=self.employee, body="Details")
        ticket.status = Status.CANCELLED
        ticket.full_clean()
        ticket.save()
        ticket.refresh_from_db()
        self.assertEqual(ticket.assigned_to, self.technician)
        self.assertTrue(ticket.comments.filter(pk=comment.pk).exists())
        with self.assertRaises(ProtectedError):
            self.category.delete()

    def test_schema_matches_erd_fields_relationships_and_constraints(self):
        expected = {
            Department: {"id", "name"}, Category: {"id", "name", "description"},
            Ticket: {"id", "title", "description", "category", "department", "requester", "assigned_to", "priority", "status", "resolution_note", "created_at", "updated_at", "resolved_at"},
            TicketComment: {"id", "ticket", "author", "body", "created_at"},
        }
        for model, fields in expected.items():
            self.assertEqual({f.name for f in model._meta.fields}, fields)
            self.assertIsInstance(model._meta.pk, models.BigAutoField)
        self.assertEqual(set(apps.get_app_config("tickets").get_models()), set(expected))
        self.assertEqual(Ticket._meta.get_field("title").max_length, 150)
        self.assertEqual(Ticket._meta.get_field("priority").max_length, 10)
        self.assertEqual(Ticket._meta.get_field("status").max_length, 20)
        self.assertFalse(Ticket._meta.get_field("resolution_note").null)
        self.assertTrue(Ticket._meta.get_field("resolved_at").null)
        for field in ("category", "department", "requester", "assigned_to"):
            self.assertIs(Ticket._meta.get_field(field).remote_field.on_delete, models.PROTECT)
            if field != "assigned_to":
                self.assertFalse(Ticket._meta.get_field(field).null)
        self.assertTrue(Ticket._meta.get_field("assigned_to").null)
        self.assertIs(TicketComment._meta.get_field("ticket").remote_field.on_delete, models.CASCADE)
        self.assertIs(TicketComment._meta.get_field("author").remote_field.on_delete, models.PROTECT)
        with connection.cursor() as cursor:
            columns = {c.name for c in connection.introspection.get_table_description(cursor, Ticket._meta.db_table)}
            constraints = connection.introspection.get_constraints(cursor, Ticket._meta.db_table)
        self.assertEqual(columns, {f.column for f in Ticket._meta.fields})
        for name in ("ticket_valid_status", "ticket_valid_priority", "ticket_assignment_matches_status", "ticket_resolution_matches_status"):
            self.assertTrue(constraints[name]["check"])
        for column, parent in (("category_id", "tickets_category"), ("department_id", "tickets_department"),
                               ("requester_id", "auth_user"), ("assigned_to_id", "auth_user")):
            self.assertTrue(any(item["foreign_key"] == (parent, "id") and item["columns"] == [column]
                                for item in constraints.values()))
