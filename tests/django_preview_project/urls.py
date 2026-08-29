from django.conf import settings
from django.urls import include, path

urlpatterns = []

if getattr(settings, "CODEX_PREVIEW_ENABLED", False):
    urlpatterns += [
        path("__codex_preview__/", include("django_codex_preview.urls")),
    ]
