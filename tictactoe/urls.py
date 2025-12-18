"""Root URL configuration for Tic-Tac-Toe."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("game.urls")),
]
