from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/importazione/", permanent=False)),
    path("admin/", admin.site.urls),
    path("importazione/", include("importazione.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

