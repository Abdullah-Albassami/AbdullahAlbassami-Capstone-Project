"""Authentication, application workflow and guarded organization setup."""

from django.contrib import admin
from django.urls import include, path
from tickets.views import ApplicationLoginView, ApplicationLogoutView

urlpatterns = [
    path("accounts/login/", ApplicationLoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", ApplicationLogoutView.as_view(), name="logout"),
    # The admin's existing logout URL shares the same feedback/privacy boundary.
    path("admin/logout/", ApplicationLogoutView.as_view()),
    path("admin/", admin.site.urls),
    path("", include("tickets.urls")),
]

handler403 = "tickets.views.permission_denied"
handler404 = "tickets.views.page_not_found"
handler500 = "tickets.views.server_error"

admin.site.site_header = "HelpDesk Pro administration"
admin.site.site_title = "HelpDesk Pro"
admin.site.index_title = "Organization setup"
