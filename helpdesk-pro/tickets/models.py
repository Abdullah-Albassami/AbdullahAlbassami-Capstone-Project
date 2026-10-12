"""The four approved entities and persisted business invariants."""

from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from django.db.models import Q

from .constants import ACTIVE_STATUSES, TERMINAL_STATUSES, Priority, Status


def trim_required(instance, *fields):
    errors = {}
    for field in fields:
        value = getattr(instance, field)
        value = value.strip() if isinstance(value, str) else value
        setattr(instance, field, value)
        if not value:
            errors[field] = "Enter meaningful text; whitespace alone is not allowed."
    return errors


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        errors = trim_required(self, "name")
        if errors:
            raise ValidationError(errors)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        errors = trim_required(self, "name")
        if isinstance(self.description, str):
            self.description = self.description.strip()
        if self.description is None:
            errors["description"] = "Use empty text rather than a null description."
        if errors:
            raise ValidationError(errors)


class Ticket(models.Model):
    Status = Status
    Priority = Priority

    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="tickets")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="tickets")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="submitted_tickets"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assigned_tickets",
        null=True, blank=True,
    )
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    resolution_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-id")
        constraints = [
            models.CheckConstraint(condition=Q(status__in=Status.values), name="ticket_valid_status"),
            models.CheckConstraint(condition=Q(priority__in=Priority.values), name="ticket_valid_priority"),
            models.CheckConstraint(
                condition=(
                    Q(status=Status.NEW, assigned_to__isnull=True)
                    | Q(status__in=(Status.ASSIGNED, Status.IN_PROGRESS, Status.RESOLVED), assigned_to__isnull=False)
                    | Q(status=Status.CANCELLED)
                ),
                name="ticket_assignment_matches_status",
            ),
            models.CheckConstraint(
                condition=(
                    (Q(status=Status.RESOLVED, resolved_at__isnull=False) & ~Q(resolution_note=""))
                    | (~Q(status=Status.RESOLVED) & Q(resolved_at__isnull=True, resolution_note=""))
                ),
                name="ticket_resolution_matches_status",
            ),
        ]

    @property
    def reference(self):
        return f"HD-{self.pk:05d}" if self.pk is not None else "Unsaved ticket"

    @property
    def is_active(self):
        return self.status in ACTIVE_STATUSES

    def __str__(self):
        return f"{self.reference}: {self.title}"

    def clean(self):
        super().clean()
        errors = trim_required(self, "title", "description")
        if isinstance(self.resolution_note, str):
            self.resolution_note = self.resolution_note.strip()
        rules = []
        if self.resolution_note is None:
            rules.append("Use empty text rather than a null resolution note.")
        if self.status == Status.NEW and self.assigned_to_id is not None:
            rules.append("New tickets cannot have an assignee; use the assignment action.")
        if self.status in (Status.ASSIGNED, Status.IN_PROGRESS, Status.RESOLVED) and not self.assigned_to_id:
            rules.append("This status requires an assigned technician.")
        if self.status == Status.RESOLVED:
            if not self.resolution_note or self.resolved_at is None:
                rules.append("Resolution requires a meaningful note and resolution timestamp.")
        elif self.resolution_note or self.resolved_at is not None:
            rules.append("Only resolved tickets may contain resolution information.")
        if self.status in ACTIVE_STATUSES and isinstance(self.assigned_to_id, int):
            from .permissions import eligible_technicians

            if not eligible_technicians().filter(pk=self.assigned_to_id).exists():
                rules.append("Assign an active account with exactly the Technician application role.")
        if self.pk and not self._state.adding:
            previous = type(self).objects.filter(pk=self.pk).first()
            if previous and previous.status in TERMINAL_STATUSES:
                immutable = (
                    "title", "description", "category_id", "department_id", "requester_id",
                    "assigned_to_id", "priority", "status", "resolution_note", "resolved_at", "created_at",
                )
                if any(getattr(previous, field) != getattr(self, field) for field in immutable):
                    rules.append("Resolved and cancelled tickets are read-only.")
        if rules:
            errors[NON_FIELD_ERRORS] = rules
        if errors:
            raise ValidationError(errors)


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ticket_comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at", "id")

    def __str__(self):
        return f"Comment on {self.ticket.reference} by {self.author}"

    def clean(self):
        super().clean()
        errors = trim_required(self, "body")
        rules = []
        if self._state.adding and isinstance(self.ticket_id, int):
            ticket = Ticket.objects.filter(pk=self.ticket_id).first()
            if ticket and not ticket.is_active:
                rules.append("Comments can only be added to active tickets.")
            if ticket and isinstance(self.author_id, int):
                from .permissions import ticket_permissions

                author = self._meta.get_field("author").remote_field.model.objects.filter(pk=self.author_id).first()
                if author and not ticket_permissions(author, ticket)["comment"]:
                    rules.append("The author cannot comment on this ticket.")
        elif self.pk:
            previous = type(self).objects.filter(pk=self.pk).first()
            if previous and any(
                getattr(previous, field) != getattr(self, field)
                for field in ("ticket_id", "author_id", "body", "created_at")
            ):
                rules.append("Comments are immutable.")
        if rules:
            errors[NON_FIELD_ERRORS] = rules
        if errors:
            raise ValidationError(errors)
