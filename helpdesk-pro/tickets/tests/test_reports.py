from io import StringIO
import os
from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.db import connection
from django.test import TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from tickets import queries, services
from tickets.constants import Role, Status
from tickets.models import Category, Ticket

from .helpers import FAST_HASHERS, TEST_PASSWORD


@override_settings(PASSWORD_HASHERS=FAST_HASHERS)
class ReportingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        with patch.dict(os.environ, DEMO_PASSWORD=TEST_PASSWORD):
            call_command("seed_demo", stdout=StringIO())
        cls.admin = User.objects.get(username="itadmin")
        cls.employee = User.objects.get(username="employee1")
        cls.technician = User.objects.get(username="technician1")
        cls.technician2 = User.objects.get(username="technician2")

    def test_known_seed_metrics_are_integrated_in_admin_dashboard(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("tickets:dashboard"))
        self.assertEqual(response.context["counts"], {"total": 12, "active": 8, "resolved": 2, "cancelled": 2})
        self.assertEqual({row["status"]: row["count"] for row in response.context["status_breakdown"]},
                         {"new": 3, "assigned": 3, "in_progress": 2, "resolved": 2, "cancelled": 2})
        self.assertEqual({category.name: category.open_ticket_count for category in response.context["categories"]},
                         {"Hardware": 3, "Software": 2, "Network": 2, "Accounts": 1, "Unused": 0})
        self.assertEqual({technician.username: technician.active_assigned_count for technician in response.context["technicians"]},
                         {"technician1": 3, "technician2": 2})
        for label in ("Status breakdown", "Category backlog", "Technician workload", "not actual availability", "Unused"):
            self.assertContains(response, label)

    def test_category_annotation_is_rendered_in_list_and_detail(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("tickets:category_list"))
        self.assertEqual({c.name: c.open_ticket_count for c in response.context["categories"]},
                         {"Hardware": 3, "Software": 2, "Network": 2, "Accounts": 1, "Unused": 0})
        self.assertContains(response, "Active tickets by category")
        response = self.client.get(reverse("tickets:category_detail", args=[1201]))
        self.assertEqual(response.context["category"].open_ticket_count, 3)
        self.assertContains(response, "Active tickets: 3")

    def test_employee_and_technician_reports_remain_strictly_scoped(self):
        for actor, expected, statuses in (
            (self.employee, {"total": 6, "active": 4, "resolved": 1, "cancelled": 1}, {"new": 2, "assigned": 1, "in_progress": 1, "resolved": 1, "cancelled": 1}),
            (self.technician, {"total": 4, "active": 3, "resolved": 1, "cancelled": 0}, {"new": 0, "assigned": 2, "in_progress": 1, "resolved": 1, "cancelled": 0}),
            (self.technician2, {"total": 4, "active": 2, "resolved": 1, "cancelled": 1}, {"new": 0, "assigned": 1, "in_progress": 1, "resolved": 1, "cancelled": 1}),
        ):
            self.client.force_login(actor)
            response = self.client.get(reverse("tickets:dashboard"))
            self.assertEqual(response.context["counts"], expected)
            self.assertEqual({row["status"]: row["count"] for row in response.context["status_breakdown"]}, statuses)
            self.assertNotIn("categories", response.context)
            self.assertNotIn("technicians", response.context)
            self.assertNotContains(response, "Category backlog")
            self.assertNotContains(response, "Technician workload")
            self.assertNotContains(response, reverse("tickets:category_list"))
            self.assertEqual(self.client.get(reverse("tickets:category_list")).status_code, 403)

    def test_query_helpers_guard_organization_reports_before_evaluation(self):
        for actor in (self.employee, self.technician):
            for report in (queries.category_backlog, queries.technician_workload):
                with self.assertRaises(PermissionDenied):
                    report(actor)
        self.assertEqual(queries.ticket_summary(self.employee)["counts"]["total"], 6)

    def test_zero_workload_and_multiple_groups_comments_do_not_inflate_counts(self):
        zero = User.objects.create_user("zero-tech", password=TEST_PASSWORD)
        zero.groups.add(Group.objects.get(name=Role.TECHNICIAN))
        for name in ("Device team", "Printer team", "Remote team"):
            self.technician.groups.add(Group.objects.create(name=name))
        for index in range(5):
            services.add_comment(self.technician, 10007, f"Diagnostic step {index}")
        self.assertEqual({c.name: c.open_ticket_count for c in queries.category_backlog(self.admin)},
                         {"Hardware": 3, "Software": 2, "Network": 2, "Accounts": 1, "Unused": 0})
        self.assertEqual({u.username: u.active_assigned_count for u in queries.technician_workload(self.admin)},
                         {"technician1": 3, "technician2": 2, "zero-tech": 0})
        self.assertEqual(queries.ticket_summary(self.admin)["counts"]["total"], 12)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("tickets:dashboard")), "zero-tech")

    def test_technician_eligibility_excludes_inactive_conflicting_and_superuser_accounts(self):
        technician_group = Group.objects.get(name=Role.TECHNICIAN)
        inactive = User.objects.create_user("inactive-tech", is_active=False)
        inactive.groups.add(technician_group)
        conflicting = User.objects.create_user("conflicting-tech")
        conflicting.groups.add(technician_group)
        User.groups.through.objects.create(user_id=conflicting.pk, group_id=Group.objects.get(name=Role.EMPLOYEE).pk)
        root = User.objects.create_superuser("root", password=TEST_PASSWORD)
        root.groups.add(technician_group)
        self.assertEqual({u.username for u in queries.technician_workload(self.admin)}, {"technician1", "technician2"})
        self.client.force_login(root)
        self.assertContains(self.client.get(reverse("tickets:dashboard")), "Technician workload")

    def test_completely_empty_ticket_category_and_technician_reports(self):
        Ticket.objects.all().delete()  # privileged fixture cleanup, not application deletion
        Category.objects.all().delete()
        for user in (self.technician, self.technician2):
            user.groups.clear()
        self.client.force_login(self.admin)
        response = self.client.get(reverse("tickets:dashboard"))
        self.assertEqual(response.context["counts"], {"total": 0, "active": 0, "resolved": 0, "cancelled": 0})
        self.assertEqual([row["count"] for row in response.context["status_breakdown"]], [0] * 5)
        self.assertEqual(list(response.context["categories"]), [])
        self.assertEqual(list(response.context["technicians"]), [])
        for message in ("No categories yet", "No eligible technicians", "No tickets yet"):
            self.assertContains(response, message)

    def test_single_status_dataset_displays_zero_for_every_absent_status(self):
        Ticket.objects.exclude(status=Status.NEW).delete()
        summary = queries.ticket_summary(self.admin)
        self.assertEqual(summary["counts"], {"total": 3, "active": 3, "resolved": 0, "cancelled": 0})
        self.assertEqual([row["count"] for row in summary["status_breakdown"]], [3, 0, 0, 0, 0])

    def test_status_cards_and_breakdown_share_one_aggregate_query(self):
        with CaptureQueriesContext(connection) as captured:
            queries.ticket_summary(self.admin)
        ticket_queries = [q["sql"] for q in captured if 'FROM "tickets_ticket"' in q["sql"]]
        self.assertEqual(len(ticket_queries), 1)
        self.assertIn("COUNT(", ticket_queries[0])

    def test_reports_update_after_creation_assignment_start_resolution_and_cancel(self):
        ticket = services.create_ticket(self.employee, {"title": "Display unavailable", "description": "Display stopped working.",
            "category": Category.objects.get(pk=1201), "department": Ticket.objects.get(pk=10001).department, "priority": "high"})
        self.assertEqual(queries.ticket_summary(self.admin)["counts"], {"total": 13, "active": 9, "resolved": 2, "cancelled": 2})
        self.assertEqual(queries.category_backlog(self.admin).get(pk=1201).open_ticket_count, 4)
        services.assign_ticket(self.admin, ticket.pk, self.technician2)
        self.assertEqual(queries.technician_workload(self.admin).get(pk=self.technician2.pk).active_assigned_count, 3)
        services.start_ticket(self.technician2, ticket.pk)
        self.assertEqual({row["status"]: row["count"] for row in queries.ticket_summary(self.admin)["status_breakdown"]}["in_progress"], 3)
        services.resolve_ticket(self.technician2, ticket.pk, "Replaced damaged cable")
        self.assertEqual(queries.ticket_summary(self.admin)["counts"], {"total": 13, "active": 8, "resolved": 3, "cancelled": 2})
        self.assertEqual(queries.category_backlog(self.admin).get(pk=1201).open_ticket_count, 3)
        self.assertEqual(queries.technician_workload(self.admin).get(pk=self.technician2.pk).active_assigned_count, 2)
        services.cancel_ticket(self.admin, 10001)
        self.assertEqual(queries.ticket_summary(self.admin)["counts"], {"total": 13, "active": 7, "resolved": 3, "cancelled": 3})
        self.client.force_login(self.admin)
        response = self.client.get(reverse("tickets:dashboard"))
        self.assertEqual(response.context["counts"]["active"], 7)
        self.assertEqual({c.name: c.open_ticket_count for c in response.context["categories"]}["Hardware"], 2)

    def test_category_report_count_stays_correct_when_terminal_category_is_deleted_attempt(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("tickets:category_delete", args=[1201]))
        self.assertContains(response, "cannot be deleted")
        response = self.client.get(reverse("tickets:category_list"))
        self.assertEqual({c.name: c.open_ticket_count for c in response.context["categories"]}["Hardware"], 3)
