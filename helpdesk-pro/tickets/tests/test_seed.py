from io import StringIO
import os
import secrets
from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Count, Q
from django.test import TestCase, override_settings

from tickets.constants import ACTIVE_STATUSES, Role
from tickets.models import Category, Department, Ticket, TicketComment
from tickets.permissions import eligible_technicians

from .helpers import FAST_HASHERS, TEST_PASSWORD


@override_settings(PASSWORD_HASHERS=FAST_HASHERS)
class SeedTests(TestCase):
    def seed(self, password=TEST_PASSWORD):
        output = StringIO()
        with patch.dict(os.environ):
            if password is None:
                os.environ.pop("DEMO_PASSWORD", None)
            else:
                os.environ["DEMO_PASSWORD"] = password
            call_command("seed_demo", stdout=output)
        self.assertNotIn(TEST_PASSWORD, output.getvalue())
        return output.getvalue()

    def test_realistic_seed_known_totals_relationships_and_historical_comments(self):
        self.seed()
        self.assertEqual((Department.objects.count(), Category.objects.count(), User.objects.count(), Ticket.objects.count(), TicketComment.objects.count()),
                         (4, 5, 5, 12, 4))
        totals = Ticket.objects.aggregate(total=Count("id"), active=Count("id", filter=Q(status__in=ACTIVE_STATUSES)),
                                         resolved=Count("id", filter=Q(status="resolved")), cancelled=Count("id", filter=Q(status="cancelled")))
        self.assertEqual(totals, {"total": 12, "active": 8, "resolved": 2, "cancelled": 2})
        categories = Category.objects.annotate(active=Count("tickets", filter=Q(tickets__status__in=ACTIVE_STATUSES)))
        self.assertEqual(dict(categories.values_list("name", "active")), {"Hardware": 3, "Software": 2, "Network": 2, "Accounts": 1, "Unused": 0})
        technicians = eligible_technicians().annotate(active=Count("assigned_tickets", filter=Q(assigned_tickets__status__in=ACTIVE_STATUSES), distinct=True))
        self.assertEqual(dict(technicians.values_list("username", "active")), {"technician1": 3, "technician2": 2})
        resolved = Ticket.objects.get(pk=10009)
        self.assertLess(resolved.comments.get().created_at, resolved.resolved_at)
        self.assertTrue(all(t.created_at <= t.updated_at for t in Ticket.objects.all()))
        self.assertTrue(all(user.check_password(TEST_PASSWORD) for user in User.objects.all()))
        self.assertFalse(User.objects.filter(is_superuser=True).exists())
        self.assertEqual(list(User.objects.get(username="itadmin").groups.values_list("name", flat=True)), [Role.IT_ADMIN])
        for ticket in Ticket.objects.all():
            ticket.full_clean()
        for comment in TicketComment.objects.all():
            comment.full_clean()

    def test_repeat_without_password_preserves_every_record_and_password(self):
        self.seed()
        before = {model: list(model.objects.order_by("pk").values()) for model in (User, Category, Department, Ticket, TicketComment)}
        output = self.seed(password=None)
        self.assertIn("0 new tickets", output)
        for model, records in before.items():
            self.assertEqual(list(model.objects.order_by("pk").values()), records)
        self.assertEqual(Group.objects.filter(name__in=Role.values).count(), 3)

    def test_user_edits_renamed_categories_and_password_changes_are_not_reset(self):
        self.seed()
        ticket = Ticket.objects.get(pk=10001)
        ticket.title = "Updated by requester"
        ticket.priority = "low"
        ticket.full_clean()
        ticket.save()
        category = Category.objects.get(pk=1201)
        category.name = "Equipment"
        category.full_clean()
        category.save()
        department = Department.objects.get(pk=1101)
        department.name = "Accounting"
        department.full_clean()
        department.save()
        user = User.objects.get(pk=9001)
        changed_password = secrets.token_urlsafe(24)
        user.username, user.first_name = "renamed_employee", "Changed"
        user.set_password(changed_password)
        user.save()
        self.seed(password=None)
        ticket.refresh_from_db()
        category.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual((ticket.title, ticket.priority, category.name, user.first_name),
                         ("Updated by requester", "low", "Equipment", "Changed"))
        self.assertTrue(user.check_password(changed_password))
        self.assertEqual((Category.objects.count(), Department.objects.count(), Ticket.objects.count()), (5, 4, 12))

    def test_missing_or_weak_runtime_password_is_atomic(self):
        for password in (None, "1" * 3):
            with self.subTest(password_provided=bool(password)):
                with self.assertRaises(CommandError):
                    self.seed(password=password)
                self.assertFalse(User.objects.exists())
                self.assertFalse(Category.objects.exists())
                self.assertFalse(Ticket.objects.exists())

    def test_reserved_username_collision_never_adopts_or_promotes_account(self):
        user = User.objects.create_user("itadmin", password=TEST_PASSWORD)
        with self.assertRaises(CommandError):
            self.seed()
        user.refresh_from_db()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.groups.exists())
        self.assertFalse(Ticket.objects.exists())

    def test_reserved_user_id_collision(self):
        user = User.objects.create_user("unrelated", password=TEST_PASSWORD, id=9001)
        with self.assertRaises(CommandError):
            self.seed()
        self.assertEqual(User.objects.get(pk=user.pk).username, "unrelated")
        self.assertEqual(User.objects.count(), 1)

    def test_reserved_category_id_collision(self):
        Category.objects.create(pk=1201, name="Unrelated category")
        with self.assertRaises(CommandError):
            self.seed()
        self.assertFalse(User.objects.exists())
        self.assertEqual(Category.objects.count(), 1)

    def test_existing_reference_name_collision_does_not_duplicate_or_overwrite(self):
        department = Department.objects.create(name="Finance")
        with self.assertRaises(CommandError):
            self.seed()
        self.assertTrue(Department.objects.filter(pk=department.pk, name="Finance").exists())
        self.assertFalse(User.objects.exists())

    def test_reserved_ticket_collision_is_detected_before_data_mutation(self):
        user = User.objects.create_user("local", password=TEST_PASSWORD)
        user.groups.add(Group.objects.get(name=Role.EMPLOYEE))
        category = Category.objects.create(name="Local category")
        department = Department.objects.create(name="Local department")
        Ticket.objects.create(pk=10001, title="Local issue", description="Keep this record", requester=user,
                              category=category, department=department)
        with self.assertRaises(CommandError):
            self.seed()
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Ticket.objects.get(pk=10001).title, "Local issue")

    def test_comment_collision_rolls_back_all_other_missing_fixture_creations(self):
        self.seed()
        TicketComment.objects.filter(pk=20001).update(created_at=Ticket.objects.get(pk=10001).created_at)
        Category.objects.get(pk=1205).delete()
        with self.assertRaises(CommandError):
            self.seed(password=None)
        self.assertFalse(Category.objects.filter(pk=1205).exists())

    def test_zero_workload_and_empty_reporting_math(self):
        empty = Ticket.objects.aggregate(total=Count("id"), active=Count("id", filter=Q(status__in=ACTIVE_STATUSES)))
        self.assertEqual(empty, {"total": 0, "active": 0})
        self.seed()
        user = User.objects.create_user("zero_technician", password=TEST_PASSWORD)
        user.groups.add(Group.objects.get(name=Role.TECHNICIAN), Group.objects.create(name="Unrelated team"))
        technicians = eligible_technicians().annotate(active=Count("assigned_tickets", filter=Q(assigned_tickets__status__in=ACTIVE_STATUSES), distinct=True))
        self.assertEqual(technicians.get(pk=user.pk).active, 0)
        self.assertEqual(technicians.get(username="technician1").active, 3)

    def test_late_validation_failure_rolls_back_reference_data_creation(self):
        self.seed()
        # Privileged maintenance creates a partial fixture requiring an invalid
        # assignment repair. The command must not partially recreate categories.
        Ticket.objects.filter(assigned_to_id=9003, status__in=ACTIVE_STATUSES).update(status="cancelled")
        technician = User.objects.get(pk=9003)
        technician.is_active = False
        technician.save()
        Ticket.objects.get(pk=10004).delete()
        Category.objects.get(pk=1205).delete()
        with self.assertRaises(CommandError):
            self.seed(password=None)
        self.assertFalse(Category.objects.filter(pk=1205).exists())
        self.assertFalse(Ticket.objects.filter(pk=10004).exists())

    def test_missing_historical_comment_never_reopens_terminal_ticket(self):
        self.seed()
        TicketComment.objects.get(pk=20004).delete()  # privileged maintenance
        with self.assertRaises(CommandError):
            self.seed(password=None)
        self.assertEqual(Ticket.objects.get(pk=10009).status, "resolved")
        self.assertFalse(TicketComment.objects.filter(pk=20004).exists())
