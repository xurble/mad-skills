from django.apps import AppConfig


class DjangoCodexPreviewConfig(AppConfig):
    name = "django_codex_preview"
    verbose_name = "Codex Django template preview"

    def ready(self) -> None:
        from . import checks  # noqa: F401
