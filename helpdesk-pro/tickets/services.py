"""Validated workflow mutations; HTTP views never save tickets directly."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .constants import Role, Status
from .models import Ticket, TicketComment
from .permissions import get_role, is_eligible_technician, require_role, ticket_permissions, visible_tickets

BUSINESS_FIELDS = frozenset(("title", "description", "category", "department", "priority"))


class WorkflowConflict(Exception):
    """The current persisted state cannot perform the requested transition."""


def get_visible_ticket(actor, pk):
    return get_object_or_404(
        visible_tickets(actor).select_related("requester", "assigned_to", "category", "department"), pk=pk
    )


def authorize_action(actor, ticket, action):
    """Shared GET/POST gate. Mutations call it again on freshly fetched state."""
    role = get_role(actor)
    if not ticket_permissions(actor, ticket)["view"]:
        # Services retrieve through the scoped queryset before calling this gate.
        raise PermissionDenied("You cannot access this ticket.")
    if action == "assign" and role != Role.IT_ADMIN:
        raise PermissionDenied("Only IT Admin can assign tickets.")
    if action in ("edit", "cancel") and role == Role.TECHNICIAN:
        raise PermissionDenied("Technicians cannot edit or cancel tickets.")
    if action in ("start", "resolve") and role == Role.EMPLOYEE:
        raise PermissionDenied("Only the assigned technician or IT Admin can perform this action.")
    if not ticket.is_active:
        raise WorkflowConflict("Resolved and cancelled tickets are read-only. This action was not applied.")
    if not ticket_permissions(actor, ticket)[action]:
        if action in ("start", "resolve"):
            expected = "Assigned" if action == "start" else "In progress"
            raise WorkflowConflict(f"This action requires a ticket in {expected} status. Refresh the ticket to continue.")
        raise PermissionDenied("Employees can edit or cancel only their own unassigned New tickets.")


def apply_business_fields(ticket, values):
    if set(values) != BUSINESS_FIELDS:
        raise ValidationError("Provide exactly the five editable ticket fields.")
    for field in BUSINESS_FIELDS:
        setattr(ticket, field, values[field])


def save_validated(ticket):
    ticket.full_clean()
    ticket.save()
    return ticket


@transaction.atomic
def create_ticket(actor, values):
    require_role(actor, Role.EMPLOYEE, Role.IT_ADMIN)
    ticket = Ticket(requester=actor)
    apply_business_fields(ticket, values)
    return save_validated(ticket)


@transaction.atomic
def update_ticket(actor, pk, values):
    ticket = get_visible_ticket(actor, pk)
    authorize_action(actor, ticket, "edit")
    apply_business_fields(ticket, values)
    return save_validated(ticket)


@transaction.atomic
def assign_ticket(actor, pk, technician):
    ticket = get_visible_ticket(actor, pk)
    authorize_action(actor, ticket, "assign")
    if not is_eligible_technician(technician):
        raise ValidationError({"assigned_to": "Choose an active account with exactly the Technician role."})
    ticket.assigned_to = technician
    if ticket.status == Status.NEW:
        ticket.status = Status.ASSIGNED
    return save_validated(ticket)


@transaction.atomic
def start_ticket(actor, pk):
    ticket = get_visible_ticket(actor, pk)
    authorize_action(actor, ticket, "start")
    ticket.status = Status.IN_PROGRESS
    return save_validated(ticket)


@transaction.atomic
def resolve_ticket(actor, pk, resolution_note):
    ticket = get_visible_ticket(actor, pk)
    authorize_action(actor, ticket, "resolve")
    ticket.status = Status.RESOLVED
    ticket.resolution_note = resolution_note
    ticket.resolved_at = timezone.now()
    return save_validated(ticket)


@transaction.atomic
def cancel_ticket(actor, pk):
    ticket = get_visible_ticket(actor, pk)
    authorize_action(actor, ticket, "cancel")
    ticket.status = Status.CANCELLED
    return save_validated(ticket)


@transaction.atomic
def add_comment(actor, pk, body):
    ticket = get_visible_ticket(actor, pk)
    authorize_action(actor, ticket, "comment")
    comment = TicketComment(ticket=ticket, author=actor, body=body)
    comment.full_clean()
    comment.save()
    return comment
