import secrets

from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings

from tickets.constants import Role
from tickets.models import Category, Department, Ticket

TEST_PASSWORD = secrets.token_urlsafe(24)
FAST_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@override_settings(PASSWORD_HASHERS=FAST_HASHERS)
class FoundationCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.groups = {role: Group.objects.get(name=role) for role in Role}
        cls.employee = cls.make_user("requester", Role.EMPLOYEE)
        cls.other = cls.make_user("other", Role.EMPLOYEE)
        cls.technician = cls.make_user("support", Role.TECHNICIAN)
        cls.technician2 = cls.make_user("support2", Role.TECHNICIAN)
        cls.itadmin = cls.make_user("manager", Role.IT_ADMIN, is_staff=True)
        cls.superuser = User.objects.create_superuser("root", password=TEST_PASSWORD)
        cls.staff = User.objects.create_user("staff", password=TEST_PASSWORD, is_staff=True)
        cls.category = Category.objects.create(name="Test category")
        cls.department = Department.objects.create(name="Test department")

    @classmethod
    def make_user(cls, username, role, **flags):
        user = User.objects.create_user(username, password=TEST_PASSWORD, **flags)
        user.groups.add(cls.groups[role])
        return user

    def make_ticket(self, **changes):
        values = dict(title="Printer unavailable", description="The printer cannot print invoices.",
                      requester=self.employee, category=self.category, department=self.department)
        values.update(changes)
        ticket = Ticket(**values)
        ticket.full_clean()
        ticket.save()
        return ticket
