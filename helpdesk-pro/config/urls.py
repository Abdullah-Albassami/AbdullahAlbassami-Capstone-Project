"""Project routes. Application routes are added in the workflow checkpoint."""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_header = "HelpDesk Pro administration"
admin.site.site_title = "HelpDesk Pro"
admin.site.index_title = "Organization setup"
