"""Guard existing auth mutations; no ticket workflow is implemented with signals."""

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_migrate, pre_delete, pre_save

from .accounts import ensure_role_groups, validate_account
from .constants import Role


def provision_roles(sender, using, **kwargs):
    ensure_role_groups(using)


def guard_account_save(sender, instance, raw, using, update_fields, **kwargs):
    if raw or not instance.pk:
        return
    if update_fields is not None and not {"is_active", "is_superuser"}.intersection(update_fields):
        return
    roles = instance.groups.using(using).values_list("name", flat=True)
    validate_account(instance, roles, using=using)


def guard_membership(sender, instance, action, reverse, pk_set, using, **kwargs):
    if action not in ("pre_add", "pre_remove", "pre_clear"):
        return
    if reverse:
        users = instance.user_set.using(using).all() if action == "pre_clear" else User.objects.using(using).filter(pk__in=pk_set)
        changed_group_ids = {instance.pk}
    else:
        users = User.objects.using(using).filter(pk=instance.pk)
        changed_group_ids = set(pk_set or ())
    for user in users:
        group_ids = set(user.groups.using(using).values_list("pk", flat=True))
        if action == "pre_add":
            group_ids |= changed_group_ids
        elif action == "pre_remove" or reverse:
            group_ids -= changed_group_ids
        else:
            group_ids.clear()
        roles = Group.objects.using(using).filter(pk__in=group_ids).values_list("name", flat=True)
        validate_account(user, roles, using=using)


def guard_group_save(sender, instance, raw, using, **kwargs):
    if raw or not instance.pk:
        return
    old_name = Group.objects.using(using).filter(pk=instance.pk).values_list("name", flat=True).first()
    if old_name and old_name != instance.name and (old_name in Role.values or instance.name in Role.values):
        raise ValidationError("Application role group names are reserved and cannot be changed.")


def guard_group_delete(sender, instance, using, **kwargs):
    persisted_name = Group.objects.using(using).filter(pk=instance.pk).values_list("name", flat=True).first()
    if persisted_name in Role.values:
        raise ValidationError("Application role groups cannot be deleted.")


def register_signals(app_config):
    post_migrate.connect(provision_roles, sender=app_config, dispatch_uid="tickets.provision_roles")
    pre_save.connect(guard_account_save, sender=User, dispatch_uid="tickets.guard_account_save")
    m2m_changed.connect(guard_membership, sender=User.groups.through, dispatch_uid="tickets.guard_membership")
    pre_save.connect(guard_group_save, sender=Group, dispatch_uid="tickets.guard_group_save")
    pre_delete.connect(guard_group_delete, sender=Group, dispatch_uid="tickets.guard_group_delete")
