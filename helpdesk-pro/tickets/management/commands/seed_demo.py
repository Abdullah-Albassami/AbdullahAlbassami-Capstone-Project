"""Create recognized demo fixtures atomically, without resetting existing data."""

import os
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.views.decorators.debug import sensitive_variables

from tickets.accounts import ensure_role_groups
from tickets.constants import Role, Status
from tickets.demo_data import (
    CATEGORIES, COMMENTS, DEPARTMENTS, RESOLUTIONS, SEED_TIME, TICKETS, USERS,
    comment_created_at, ticket_created_at,
)
from tickets.models import Category, Department, Ticket, TicketComment


class Command(BaseCommand):
    help = "Load fictional HelpDesk fixtures; set DEMO_PASSWORD at runtime for new accounts. Never resets existing records."

    @sensitive_variables("password")
    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                existing_users = self.preflight()
                password = os.environ.get("DEMO_PASSWORD", "")
                for pk, username, first, last, role in USERS:
                    if pk not in existing_users:
                        if not password:
                            raise CommandError("Set DEMO_PASSWORD at runtime to create demo accounts. No records were changed.")
                        validate_password(password, User(username=username, first_name=first, last_name=last))
                groups = ensure_role_groups()
                for pk, username, first, last, role in USERS:
                    if pk in existing_users:
                        continue
                    user = User(
                        pk=pk, username=username, first_name=first, last_name=last,
                        email=f"{username}@helpdesk.example", date_joined=SEED_TIME,
                        is_active=True, is_staff=role == Role.IT_ADMIN, is_superuser=False,
                    )
                    user.set_password(password)
                    user.full_clean()
                    user.save()
                    user.groups.add(groups[role])
                for pk, name in DEPARTMENTS:
                    if not Department.objects.filter(pk=pk).exists():
                        department = Department(pk=pk, name=name)
                        department.full_clean()
                        department.save()
                for pk, name, description in CATEGORIES:
                    if not Category.objects.filter(pk=pk).exists():
                        category = Category(pk=pk, name=name, description=description)
                        category.full_clean()
                        category.save()

                created = {}
                for pk, title, description, category, department, requester, priority, status, assignee in TICKETS:
                    if Ticket.objects.filter(pk=pk).exists():
                        continue
                    initial_status = status
                    if status == Status.RESOLVED:
                        initial_status = Status.IN_PROGRESS
                    elif status == Status.CANCELLED:
                        initial_status = Status.ASSIGNED if assignee else Status.NEW
                    ticket = Ticket(
                        pk=pk, title=title, description=description, category_id=category,
                        department_id=department, requester_id=requester, priority=priority,
                        status=initial_status, assigned_to_id=assignee,
                    )
                    ticket.full_clean()
                    ticket.save()
                    timestamp = ticket_created_at(pk)
                    Ticket.objects.filter(pk=pk).update(created_at=timestamp, updated_at=timestamp)
                    ticket.refresh_from_db()
                    created[pk] = (ticket, status)

                for pk, ticket_id, author_id, body in COMMENTS:
                    if TicketComment.objects.filter(pk=pk).exists():
                        continue
                    comment = TicketComment(pk=pk, ticket_id=ticket_id, author_id=author_id, body=body)
                    comment.full_clean()
                    comment.save()
                    TicketComment.objects.filter(pk=pk).update(created_at=comment_created_at(pk))

                for pk, (ticket, final_status) in created.items():
                    ticket.status = final_status
                    if final_status == Status.RESOLVED:
                        ticket.resolution_note = RESOLUTIONS[pk]
                        ticket.resolved_at = ticket.created_at + timedelta(hours=1)
                    ticket.full_clean()
                    ticket.save()
                    elapsed = {
                        Status.NEW: timedelta(), Status.ASSIGNED: timedelta(minutes=10),
                        Status.IN_PROGRESS: timedelta(minutes=30), Status.RESOLVED: timedelta(hours=1),
                        Status.CANCELLED: timedelta(hours=1),
                    }[final_status]
                    Ticket.objects.filter(pk=pk).update(updated_at=ticket.created_at + elapsed)
        except ValidationError as error:
            raise CommandError("Demo seed rejected: " + " ".join(error.messages)) from error
        self.stdout.write(self.style.SUCCESS(
            f"Demo seed complete: {len(created)} new tickets; existing records and passwords preserved."
        ))

    def preflight(self):
        """Reserved IDs plus immutable fixture timestamps establish provenance."""
        existing_users = {}
        for pk, username, *_ in USERS:
            user = User.objects.filter(pk=pk).first()
            if user:
                if user.date_joined != SEED_TIME:
                    raise CommandError(f"Reserved demo user ID {pk} is occupied by an unrelated record.")
                existing_users[pk] = user
            if User.objects.filter(username=username).exclude(pk=pk).exists():
                raise CommandError(f"Reserved demo username '{username}' already belongs to another account.")
        known_bundle = bool(existing_users)
        for model, fixtures in ((Department, DEPARTMENTS), (Category, CATEGORIES)):
            for pk, name, *_ in fixtures:
                if model.objects.filter(pk=pk).exists():
                    if not known_bundle:
                        raise CommandError(f"Reserved {model.__name__} ID {pk} is already occupied.")
                elif model.objects.filter(name=name).exists():
                    raise CommandError(f"Demo {model.__name__} name '{name}' already exists at a different ID.")
        for pk, *_ in TICKETS:
            ticket = Ticket.objects.filter(pk=pk).first()
            if ticket and ticket.created_at != ticket_created_at(pk):
                raise CommandError(f"Reserved demo ticket ID {pk} is occupied by an unrelated record.")
        for pk, ticket_id, *_ in COMMENTS:
            comment = TicketComment.objects.filter(pk=pk).first()
            if comment and (comment.created_at != comment_created_at(pk) or comment.ticket_id != ticket_id):
                raise CommandError(f"Reserved demo comment ID {pk} is occupied by an unrelated record.")
        return existing_users
