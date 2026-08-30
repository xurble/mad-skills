from django.apps import AppConfig


class MadSkillsDjangoPreviewConfig(AppConfig):
    name = "mad_skills_django_preview"
    verbose_name = "mad-skills Django template preview"

    def ready(self) -> None:
        from . import checks  # noqa: F401
