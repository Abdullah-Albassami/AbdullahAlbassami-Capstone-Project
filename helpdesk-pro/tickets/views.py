"""HTTP binding/rendering; permissions and mutations live in shared modules."""

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from . import services
from .constants import ACTIVE_STATUSES, Role, Status
from .forms import AssignmentForm, CommentForm, ResolutionForm, TicketForm, add_validation_errors
from .permissions import can_create_ticket, get_role, require_role, ticket_permissions, visible_tickets


def user_context(request):
    try:
        role = get_role(request.user)
    except PermissionDenied:
        return {}
    return {"app_role": role, "can_create": can_create_ticket(request.user),
            "can_setup": role == Role.IT_ADMIN and request.user.is_staff}


def error_page(request, status, detail):
    return render(request, "errors/error.html", {**user_context(request), "error_status": status, "error_detail": detail}, status=status)


def application_view(methods=("GET",)):
    """Authenticated role gate with usable errors even in local DEBUG mode."""
    def decorate(view):
        @login_required
        @require_http_methods(methods)
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            try:
                get_role(request.user)
                return view(request, *args, **kwargs)
            except PermissionDenied as error:
                return error_page(request, 403, str(error))
            except Http404:
                return error_page(request, 404, "This ticket is unavailable. Check the reference or return to your ticket list.")
            except services.WorkflowConflict as error:
                return error_page(request, 409, str(error))
            except ValidationError as error:
                return error_page(request, 409, " ".join(error.messages))
        return wrapped
    return decorate


@application_view()
def dashboard(request):
    tickets = visible_tickets(request.user)
    # Final query for the basic role summary. Status/category/workload reports belong to D.
    counts = tickets.aggregate(total=Count("id"), active=Count("id", filter=Q(status__in=ACTIVE_STATUSES)),
                               resolved=Count("id", filter=Q(status=Status.RESOLVED)),
                               cancelled=Count("id", filter=Q(status=Status.CANCELLED)))
    recent = tickets.select_related("category", "department", "requester", "assigned_to")[:5]
    return render(request, "tickets/dashboard.html", {**user_context(request), "counts": counts, "tickets": recent})


@application_view()
def ticket_list(request):
    tickets = visible_tickets(request.user).select_related("category", "department", "requester", "assigned_to")
    return render(request, "tickets/ticket_list.html", {**user_context(request), "tickets": tickets})


def detail_response(request, ticket, **bound_forms):
    context = {**user_context(request), "ticket": ticket, "permissions": ticket_permissions(request.user, ticket),
               "comments": ticket.comments.select_related("author"),
               "assignment_form": AssignmentForm(initial={"assigned_to": ticket.assigned_to_id}),
               "resolution_form": ResolutionForm(), "comment_form": CommentForm()}
    context.update(bound_forms)
    return render(request, "tickets/ticket_detail.html", context)


@application_view()
def ticket_detail(request, pk):
    return detail_response(request, services.get_visible_ticket(request.user, pk))


@application_view(("GET", "POST"))
def ticket_create(request):
    require_role(request.user, Role.EMPLOYEE, Role.IT_ADMIN)
    form = TicketForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            ticket = services.create_ticket(request.user, form.cleaned_data)
        except ValidationError as error:
            add_validation_errors(form, error)
        else:
            messages.success(request, f"{ticket.reference} submitted. Your ticket is New and awaiting assignment.")
            return redirect("tickets:ticket_detail", pk=ticket.pk)
    return render(request, "tickets/ticket_form.html", {**user_context(request), "form": form})


@application_view(("GET", "POST"))
def ticket_update(request, pk):
    ticket = services.get_visible_ticket(request.user, pk)
    services.authorize_action(request.user, ticket, "edit")
    form = TicketForm(request.POST if request.method == "POST" else None, instance=ticket)
    if request.method == "POST" and form.is_valid():
        try:
            saved = services.update_ticket(request.user, pk, form.cleaned_data)
        except ValidationError as error:
            add_validation_errors(form, error)
        else:
            messages.success(request, f"{saved.reference} updated.")
            return redirect("tickets:ticket_detail", pk=pk)
    return render(request, "tickets/ticket_form.html", {**user_context(request), "form": form, "ticket": ticket})


@application_view(("GET", "POST"))
def ticket_cancel(request, pk):
    ticket = services.get_visible_ticket(request.user, pk)
    services.authorize_action(request.user, ticket, "cancel")
    if request.method == "POST":
        services.cancel_ticket(request.user, pk)
        messages.success(request, f"{ticket.reference} cancelled. Its details and discussion have been retained.")
        return redirect("tickets:ticket_detail", pk=pk)
    return render(request, "tickets/ticket_cancel_confirm.html", {**user_context(request), "ticket": ticket})


@application_view(("POST",))
def ticket_assign(request, pk):
    ticket = services.get_visible_ticket(request.user, pk)
    services.authorize_action(request.user, ticket, "assign")
    form = AssignmentForm(request.POST)
    if form.is_valid():
        try:
            services.assign_ticket(request.user, pk, form.cleaned_data["assigned_to"])
        except ValidationError as error:
            add_validation_errors(form, error)
        else:
            messages.success(request, f"{ticket.reference} assigned to {form.cleaned_data['assigned_to'].get_username()}.")
            return redirect("tickets:ticket_detail", pk=pk)
    return detail_response(request, ticket, assignment_form=form)


@application_view(("POST",))
def ticket_start(request, pk):
    services.start_ticket(request.user, pk)
    messages.success(request, "Work started. The ticket is now In progress.")
    return redirect("tickets:ticket_detail", pk=pk)


@application_view(("POST",))
def ticket_resolve(request, pk):
    ticket = services.get_visible_ticket(request.user, pk)
    services.authorize_action(request.user, ticket, "resolve")
    form = ResolutionForm(request.POST)
    if form.is_valid():
        try:
            services.resolve_ticket(request.user, pk, form.cleaned_data["resolution_note"])
        except ValidationError as error:
            add_validation_errors(form, error)
        else:
            messages.success(request, f"{ticket.reference} resolved. The resolution and discussion are retained.")
            return redirect("tickets:ticket_detail", pk=pk)
    return detail_response(request, ticket, resolution_form=form)


@application_view(("POST",))
def ticket_comment(request, pk):
    ticket = services.get_visible_ticket(request.user, pk)
    services.authorize_action(request.user, ticket, "comment")
    form = CommentForm(request.POST)
    if form.is_valid():
        try:
            services.add_comment(request.user, pk, form.cleaned_data["body"])
        except ValidationError as error:
            add_validation_errors(form, error)
        else:
            messages.success(request, "Comment added.")
            return redirect("tickets:ticket_detail", pk=pk)
    return detail_response(request, ticket, comment_form=form)


def permission_denied(request, exception):
    return error_page(request, 403, "You do not have permission to access this page.")


def page_not_found(request, exception):
    return error_page(request, 404, "This page is unavailable. Return to your dashboard or ticket list.")


def server_error(request):
    # Do not query the database while handling an unexpected server/database failure.
    return render(request, "errors/error.html", {"user": AnonymousUser(), "messages": [],
        "error_status": 500, "error_detail": "Something went wrong. Please try again later."}, status=500)


def csrf_failure(request, reason=""):
    return error_page(request, 403, "Your form could not be verified. Refresh the page and submit it again.")
