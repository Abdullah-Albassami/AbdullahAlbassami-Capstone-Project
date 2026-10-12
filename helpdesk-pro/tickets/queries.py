"""Integrated scoped list queries and useful administrator reports."""

from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Case, Count, IntegerField, Q, Value, When

from .constants import ACTIVE_STATUSES, Priority, Role, Status
from .forms import TicketFilterForm
from .models import Category
from .permissions import eligible_technicians, require_role, visible_tickets


def ticket_list_page(actor, parameters):
    tickets = visible_tickets(actor)  # Scope precedes every user-selected query.
    form = TicketFilterForm(parameters)
    values = form.cleaned_data
    if values.get("q"):
        tickets = tickets.filter(Q(title__icontains=values["q"]) | Q(description__icontains=values["q"]))
    for field in ("status", "priority"):
        if values.get(field):
            tickets = tickets.filter(**{field: values[field]})
    if values.get("category"):
        tickets = tickets.filter(category__name=values["category"].name)
    order = values.get("order") or "newest"
    if order == "priority":
        tickets = tickets.alias(priority_rank=Case(
            When(priority=Priority.HIGH, then=Value(0)), When(priority=Priority.MEDIUM, then=Value(1)),
            default=Value(2), output_field=IntegerField(),
        )).order_by("priority_rank", "-created_at", "-id")
    else:
        ordering = {"newest": ("-created_at", "-id"), "oldest": ("created_at", "id"),
                    "updated": ("-updated_at", "-id")}
        tickets = tickets.order_by(*ordering[order])
    tickets = tickets.select_related("category", "department", "requester", "assigned_to")
    try:
        page_number = int(parameters.get("page", "1"))
    except (ValueError, TypeError):
        page_number = 1
    if page_number < 1 or len(parameters.getlist("page")) > 1:
        page_number = 1
    page = Paginator(tickets, 10).get_page(page_number)
    preserved = {name: values[name] for name in ("q", "status", "priority") if values.get(name)}
    if values.get("category"):
        preserved["category"] = values["category"].pk
    preserved["order"] = order
    return {"filter_form": form, "page_obj": page, "tickets": page.object_list,
            "filter_query": urlencode(preserved), "has_filters": any(values.get(name) for name in ("q", "status", "priority", "category")),
            "table_caption": f"Tickets — {dict(TicketFilterForm.ORDER_CHOICES)[order]}"}


def ticket_summary(actor):
    # One aggregate query supplies both cards and all five zero-safe status counts.
    metrics = visible_tickets(actor).aggregate(
        total=Count("id"), active=Count("id", filter=Q(status__in=ACTIVE_STATUSES)),
        **{status: Count("id", filter=Q(status=status)) for status in Status},
    )
    return {"counts": {key: metrics[key] for key in ("total", "active", "resolved", "cancelled")},
            "status_breakdown": [{"status": status, "label": label, "count": metrics[status]} for status, label in Status.choices]}


def category_backlog(actor):
    require_role(actor, Role.IT_ADMIN)
    return Category.objects.annotate(open_ticket_count=Count(
        "tickets", filter=Q(tickets__status__in=ACTIVE_STATUSES), distinct=True,
    ))


def technician_workload(actor):
    require_role(actor, Role.IT_ADMIN)
    return eligible_technicians().annotate(active_assigned_count=Count(
        "assigned_tickets", filter=Q(assigned_tickets__status__in=ACTIVE_STATUSES), distinct=True,
    ))
