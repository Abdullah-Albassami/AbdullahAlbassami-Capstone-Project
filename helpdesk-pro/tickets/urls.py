from django.urls import path

from . import views

app_name = "tickets"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/new/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/<int:pk>/edit/", views.ticket_update, name="ticket_update"),
    path("tickets/<int:pk>/cancel/", views.ticket_cancel, name="ticket_cancel"),
    path("tickets/<int:pk>/assign/", views.ticket_assign, name="ticket_assign"),
    path("tickets/<int:pk>/start/", views.ticket_start, name="ticket_start"),
    path("tickets/<int:pk>/resolve/", views.ticket_resolve, name="ticket_resolve"),
    path("tickets/<int:pk>/comment/", views.ticket_comment, name="ticket_comment"),
]
