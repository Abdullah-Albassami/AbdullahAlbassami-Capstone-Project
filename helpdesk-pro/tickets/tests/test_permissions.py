from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from tickets.constants import Role, Status
from tickets.permissions import (
    can_create_ticket, eligible_technicians, get_role, has_role, is_eligible_technician,
    require_role, ticket_permissions, visible_tickets,
)

from .helpers import FoundationCase, TEST_PASSWORD


class PermissionTests(FoundationCase):
    def test_three_roles_and_superuser_override(self):
        for user, role in ((self.employee, Role.EMPLOYEE), (self.technician, Role.TECHNICIAN),
                           (self.itadmin, Role.IT_ADMIN), (self.superuser, Role.IT_ADMIN)):
            self.assertEqual(get_role(user), role)
        self.superuser.groups.add(self.groups[Role.EMPLOYEE], self.groups[Role.TECHNICIAN])
        self.assertEqual(get_role(self.superuser), Role.IT_ADMIN)

    def test_fail_closed_anonymous_no_role_staff_inactive_and_corrupt_membership(self):
        inactive = self.make_user("inactive", Role.TECHNICIAN, is_active=False)
        User.groups.through.objects.create(user=self.technician, group=self.groups[Role.EMPLOYEE])
        for user in (AnonymousUser(), self.staff, inactive, self.technician):
            with self.subTest(account=type(user).__name__):
                with self.assertRaises(PermissionDenied):
                    get_role(user)
                with self.assertRaises(PermissionDenied):
                    visible_tickets(user)
                self.assertFalse(has_role(user, Role.IT_ADMIN))
        self.assertFalse(is_eligible_technician(inactive))

    def test_unrelated_groups_do_not_break_role_or_duplicate_eligible_users(self):
        self.technician.groups.add(Group.objects.create(name="Other team"), Group.objects.create(name="Extra team"))
        self.assertEqual(get_role(self.technician), Role.TECHNICIAN)
        self.assertEqual(list(eligible_technicians()), [self.technician, self.technician2])
        self.assertFalse(is_eligible_technician(self.superuser))

    def test_django_password_authentication_and_inactive_rejection(self):
        self.assertEqual(authenticate(username=self.employee.username, password=TEST_PASSWORD), self.employee)
        self.employee.is_active = False
        self.employee.save()
        self.assertIsNone(authenticate(username=self.employee.username, password=TEST_PASSWORD))

    def test_create_and_require_role(self):
        self.assertTrue(can_create_ticket(self.employee))
        self.assertTrue(can_create_ticket(self.itadmin))
        self.assertFalse(can_create_ticket(self.technician))
        with self.assertRaises(PermissionDenied):
            require_role(self.employee, Role.IT_ADMIN)

    def test_role_resolution_uses_current_database_flags(self):
        self.employee.is_superuser = True  # unsaved flags do not grant authority
        self.assertEqual(get_role(self.employee), Role.EMPLOYEE)
        self.staff.is_superuser = True
        with self.assertRaises(PermissionDenied):
            get_role(self.staff)
        with self.assertRaises(PermissionDenied):
            get_role(User(is_superuser=True))
        User.objects.filter(pk=self.employee.pk).update(is_active=False)
        with self.assertRaises(PermissionDenied):
            get_role(self.employee)

    def test_visibility_and_all_actions_for_new_ticket(self):
        own = self.make_ticket()
        other = self.make_ticket(requester=self.other)
        self.assertEqual(set(visible_tickets(self.employee)), {own})
        self.assertEqual(set(visible_tickets(self.itadmin)), {own, other})
        self.assertFalse(visible_tickets(self.technician).exists())
        self.assertEqual({action for action, allowed in ticket_permissions(self.employee, own).items() if allowed},
                         {"view", "edit", "cancel", "comment"})
        self.assertFalse(any(ticket_permissions(self.other, own).values()))
        self.assertFalse(any(ticket_permissions(self.technician, own).values()))

    def test_assigned_inprogress_reassignment_and_terminal_permissions(self):
        ticket = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        self.assertEqual(set(visible_tickets(self.technician)), {ticket})
        self.assertTrue(ticket_permissions(self.technician, ticket)["start"])
        self.assertFalse(ticket_permissions(self.employee, ticket)["cancel"])
        self.assertFalse(ticket_permissions(self.technician2, ticket)["view"])
        ticket.status = Status.IN_PROGRESS
        ticket.assigned_to = self.technician2
        ticket.full_clean()
        ticket.save()
        self.assertFalse(visible_tickets(self.technician).exists())
        self.assertFalse(ticket_permissions(self.technician, ticket)["view"])
        self.assertTrue(ticket_permissions(self.technician2, ticket)["resolve"])
        self.assertFalse(ticket_permissions(self.technician2, ticket)["start"])
        ticket.status = Status.CANCELLED
        ticket.full_clean()
        ticket.save()
        for user in (self.employee, self.technician2, self.itadmin):
            self.assertEqual({k for k, v in ticket_permissions(user, ticket).items() if v}, {"view"})


class AccountSafeguardTests(FoundationCase):
    def test_multiple_application_roles_rejected_forward_and_reverse(self):
        for change in (lambda: self.employee.groups.add(self.groups[Role.TECHNICIAN]),
                       lambda: self.groups[Role.TECHNICIAN].user_set.add(self.employee)):
            with self.assertRaises(ValidationError), transaction.atomic():
                change()
        self.assertEqual(get_role(self.employee), Role.EMPLOYEE)

    def test_active_assignee_cannot_be_deactivated_or_promoted(self):
        self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        for field in ("is_active", "is_superuser"):
            self.technician.refresh_from_db()
            setattr(self.technician, field, field == "is_superuser")
            with self.assertRaises(ValidationError):
                self.technician.save()
        self.technician.refresh_from_db()
        self.assertTrue(self.technician.is_active)
        self.assertFalse(self.technician.is_superuser)

    def test_active_role_removal_clear_and_reverse_clear_rejected_atomically(self):
        self.make_ticket(status=Status.IN_PROGRESS, assigned_to=self.technician)
        for action in (lambda: self.technician.groups.remove(self.groups[Role.TECHNICIAN]),
                       lambda: self.technician.groups.clear(),
                       lambda: self.groups[Role.TECHNICIAN].user_set.remove(self.technician),
                       lambda: self.groups[Role.TECHNICIAN].user_set.clear(),
                       lambda: self.technician.groups.set([self.groups[Role.EMPLOYEE]])):
            with self.assertRaises(ValidationError), transaction.atomic():
                action()
        self.assertEqual(get_role(self.technician), Role.TECHNICIAN)

    def test_reassignment_or_terminal_outcome_allows_account_change(self):
        ticket = self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        ticket.assigned_to = self.technician2
        ticket.full_clean()
        ticket.save()
        self.technician.is_active = False
        self.technician.save()
        self.technician.groups.set([self.groups[Role.EMPLOYEE]])
        ticket.status = Status.CANCELLED
        ticket.full_clean()
        ticket.save()
        self.technician2.groups.set([self.groups[Role.EMPLOYEE]])
        self.technician2.is_active = False
        self.technician2.save()
        ticket.refresh_from_db()
        self.assertEqual(ticket.assigned_to, self.technician2)

    def test_profile_password_and_nonrole_group_changes_remain_allowed(self):
        self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        self.technician.first_name = "Updated"
        self.technician.save()
        self.technician.groups.add(Group.objects.create(name="Unrelated"))
        self.technician.set_unusable_password()
        self.technician.save(update_fields=["password"])

    def test_reserved_group_rename_delete_and_masquerading_blocked(self):
        role = self.groups[Role.TECHNICIAN]
        role.name = "Renamed role"
        with self.assertRaises(ValidationError):
            role.save()
        role.refresh_from_db()
        with self.assertRaises(ValidationError), transaction.atomic():
            role.delete()
        group = Group.objects.create(name="Unrelated")
        group.name = Role.TECHNICIAN
        with self.assertRaises(ValidationError):
            group.save()

    def test_post_migration_groups_have_only_department_setup_permissions(self):
        self.assertEqual(set(self.groups[Role.IT_ADMIN].permissions.values_list("codename", flat=True)),
                         {"view_department", "add_department", "change_department", "delete_department"})
        self.assertFalse(self.groups[Role.EMPLOYEE].permissions.exists())
        self.assertFalse(self.groups[Role.TECHNICIAN].permissions.exists())

    def test_unsaved_group_rename_cannot_bypass_reserved_deletion_guard(self):
        self.make_ticket(status=Status.ASSIGNED, assigned_to=self.technician)
        group = self.groups[Role.TECHNICIAN]
        group.name = "Unsaved rename"
        with self.assertRaises(ValidationError), transaction.atomic():
            group.delete()
        self.assertEqual(get_role(self.technician), Role.TECHNICIAN)

    def test_unsaved_superuser_flag_cannot_bypass_membership_guard(self):
        self.employee.is_superuser = True
        with self.assertRaises(ValidationError), transaction.atomic():
            self.employee.groups.add(self.groups[Role.TECHNICIAN])
        self.assertEqual(list(self.employee.groups.values_list("name", flat=True)), [Role.EMPLOYEE])
