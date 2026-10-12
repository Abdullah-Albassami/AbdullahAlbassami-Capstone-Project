"""Authentication, application workflow and guarded organization setup."""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

urlpatterns = [
    path("accounts/login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("", include("tickets.urls")),
]

handler403 = "tickets.views.permission_denied"
handler404 = "tickets.views.page_not_found"
handler500 = "tickets.views.server_error"

admin.site.site_header = "HelpDesk Pro administration"
admin.site.site_title = "HelpDesk Pro"
admin.site.index_title = "Organization setup"
