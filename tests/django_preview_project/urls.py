from django.conf import settings
from django.urls import include, path

urlpatterns = []

if getattr(settings, "MAD_SKILLS_PREVIEW_ENABLED", False):
    urlpatterns += [
        path("__mad_skills_preview__/", include("mad_skills_django_preview.urls")),
    ]
