"""Forms for guarded provisioning within Django's built-in administration."""

from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .accounts import validate_account
from .constants import Role


class AccountSafeguardsMixin:
    def clean(self):
        data = super().clean()
        if "groups" not in data:
            return data
        roles = set(data["groups"].values_list("name", flat=True)) & set(Role.values)
        self.instance.is_active = data.get("is_active", self.instance.is_active)
        self.instance.is_superuser = data.get("is_superuser", self.instance.is_superuser)
        validate_account(self.instance, roles, require_role=True)
        if Role.IT_ADMIN in roles:
            data["is_staff"] = True
        return data


class GuardedUserCreationForm(AccountSafeguardsMixin, AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = User
        fields = ("username", "groups", "is_active", "is_staff", "is_superuser")


class GuardedUserChangeForm(AccountSafeguardsMixin, UserChangeForm):
    pass


class GuardedGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name", "permissions")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        old_name = Group.objects.filter(pk=self.instance.pk).values_list("name", flat=True).first()
        if old_name and old_name != name and (old_name in Role.values or name in Role.values):
            raise ValidationError("Application role names are reserved; choose a different group name.")
        return name
