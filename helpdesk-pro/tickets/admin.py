"""Django admin for organization setup and read-only ticket inspection."""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .admin_forms import GuardedGroupForm, GuardedUserChangeForm, GuardedUserCreationForm
from .constants import Role
from .models import Category, Department, Ticket, TicketComment
from .permissions import has_role


class SuperuserOnlyMixin:
    def has_module_permission(self, request):
        return bool(request.user.is_authenticated and User.objects.filter(
            pk=request.user.pk, is_active=True, is_staff=True, is_superuser=True,
        ).exists())

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    def has_module_permission(self, request):
        return has_role(request.user, Role.IT_ADMIN) and super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        return has_role(request.user, Role.IT_ADMIN) and super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        return has_role(request.user, Role.IT_ADMIN) and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return has_role(request.user, Role.IT_ADMIN) and super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return has_role(request.user, Role.IT_ADMIN) and super().has_delete_permission(request, obj)


@admin.register(Category)
class CategoryAdmin(SuperuserOnlyMixin, admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class ReadOnlyTicketAdmin(SuperuserOnlyMixin, admin.ModelAdmin):
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return tuple(field.name for field in self.model._meta.fields)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(ReadOnlyTicketAdmin):
    list_display = ("reference", "title", "status", "priority", "requester", "assigned_to")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")
    list_select_related = ("requester", "assigned_to", "category", "department")


@admin.register(TicketComment)
class TicketCommentAdmin(ReadOnlyTicketAdmin):
    list_display = ("ticket", "author", "created_at")
    list_select_related = ("ticket", "author")


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class GuardedUserAdmin(SuperuserOnlyMixin, UserAdmin):
    form = GuardedUserChangeForm
    add_form = GuardedUserCreationForm
    readonly_fields = ("last_login", "date_joined")
    add_fieldsets = (
        (None, {"fields": ("username", "usable_password", "password1", "password2")}),
        ("Application access", {"fields": ("groups", "is_active", "is_staff", "is_superuser")}),
    )
    actions = None

    def save_model(self, request, obj, form, change):
        # Reduce an allowed superuser's multiple roles before demotion. The
        # standard admin transaction then saves the final flags and memberships.
        if change and not obj.is_superuser and User.objects.filter(pk=obj.pk, is_superuser=True).exists():
            obj.groups.set(form.cleaned_data["groups"])
        super().save_model(request, obj, form, change)


@admin.register(Group)
class GuardedGroupAdmin(SuperuserOnlyMixin, GroupAdmin):
    form = GuardedGroupForm
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return ("name", "permissions") if obj and obj.name in Role.values else ()

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and not (obj and obj.name in Role.values)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and not (obj and obj.name in Role.values)
