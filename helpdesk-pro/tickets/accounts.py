"""Minimal safeguards around Django's existing accounts and role groups."""

from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

from .constants import ACTIVE_STATUSES, Role
from .models import Ticket


def ensure_role_groups(using="default"):
    groups = {role: Group.objects.using(using).get_or_create(name=role)[0] for role in Role}
    for role, group in groups.items():
        permissions = Permission.objects.using(using).filter(
            content_type__app_label="tickets", content_type__model="department",
            codename__in=("view_department", "add_department", "change_department", "delete_department"),
        ) if role == Role.IT_ADMIN else Permission.objects.using(using).none()
        group.permissions.set(permissions)
    return groups


def validate_account(user, role_names, *, require_role=False, using="default"):
    roles = set(role_names) & set(Role.values)
    if not user.is_superuser and (len(roles) > 1 or (require_role and len(roles) != 1)):
        raise ValidationError("Choose exactly one application role: Employee, Technician or IT Admin.")
    active_assignments = user.pk and Ticket.objects.using(using).filter(
        assigned_to_id=user.pk, status__in=ACTIVE_STATUSES,
    ).exists()
    if active_assignments and (not user.is_active or user.is_superuser or roles != {Role.TECHNICIAN}):
        raise ValidationError("Reassign this account's active tickets before deactivation or changing its technician role.")
