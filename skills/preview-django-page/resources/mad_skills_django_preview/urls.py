from django.urls import path

from . import checks  # noqa: F401
from .views import create_preview, render_preview

app_name = "mad_skills_django_preview"

urlpatterns = [
    path("create/", create_preview, name="create"),
    path("p/<str:preview_id>/", render_preview, name="render"),
]
