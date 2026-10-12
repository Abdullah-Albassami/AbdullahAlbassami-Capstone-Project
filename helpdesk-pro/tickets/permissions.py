"""Shared role, queryset and action rules; views must also enforce them."""

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .constants import Role, Status
from .models import Ticket


def get_role(user):
    if not getattr(user, "is_authenticated", False) or not getattr(user, "pk", None):
        raise PermissionDenied("Sign in with an active application account.")
    current = get_user_model().objects.filter(pk=user.pk, is_active=True).only("is_superuser").first()
    if current is None:
        raise PermissionDenied("Sign in with an active application account.")
    if current.is_superuser:
        return Role.IT_ADMIN
    roles = list(current.groups.filter(name__in=Role.values).values_list("name", flat=True))
    if len(roles) != 1:
        raise PermissionDenied("Your account needs exactly one application role. Contact the administrator.")
    return Role(roles[0])


def has_role(user, *roles):
    try:
        return get_role(user) in roles
    except PermissionDenied:
        return False


def require_role(user, *roles):
    role = get_role(user)
    if role not in roles:
        raise PermissionDenied("Your application role does not permit this action.")
    return role


def eligible_technicians():
    return get_user_model().objects.filter(
        is_active=True, is_superuser=False, groups__name=Role.TECHNICIAN,
    ).exclude(groups__name__in=(Role.EMPLOYEE, Role.IT_ADMIN)).distinct().order_by("username")


def is_eligible_technician(user):
    return bool(user and user.pk and eligible_technicians().filter(pk=user.pk).exists())


def visible_tickets(user):
    role = get_role(user)
    if role == Role.EMPLOYEE:
        return Ticket.objects.filter(requester=user)
    if role == Role.TECHNICIAN:
        return Ticket.objects.filter(assigned_to=user)
    return Ticket.objects.all()


def can_create_ticket(user):
    return has_role(user, Role.EMPLOYEE, Role.IT_ADMIN)


def ticket_permissions(user, ticket):
    permissions = dict.fromkeys(("view", "edit", "cancel", "assign", "start", "resolve", "comment"), False)
    try:
        role = get_role(user)
    except PermissionDenied:
        return permissions
    admin = role == Role.IT_ADMIN
    owner = role == Role.EMPLOYEE and ticket.requester_id == user.pk
    assignee = role == Role.TECHNICIAN and ticket.assigned_to_id == user.pk
    visible = admin or owner or assignee
    permissions["view"] = visible
    if not visible or not ticket.is_active:
        return permissions
    own_new = owner and ticket.status == Status.NEW and ticket.assigned_to_id is None
    permissions.update(
        edit=admin or own_new,
        cancel=admin or own_new,
        assign=admin,
        start=(admin or assignee) and ticket.status == Status.ASSIGNED and ticket.assigned_to_id is not None,
        resolve=(admin or assignee) and ticket.status == Status.IN_PROGRESS and ticket.assigned_to_id is not None,
        comment=True,
    )
    return permissions
