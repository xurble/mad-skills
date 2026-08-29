from __future__ import annotations

from typing import Any

from django.conf import settings
from django.core.checks import Critical, register


@register()
def preview_enabled_requires_debug(app_configs: Any, **kwargs: Any) -> list[Critical]:
    if getattr(settings, "CODEX_PREVIEW_ENABLED", False) is True and not settings.DEBUG:
        return [
            Critical(
                "Django Codex preview is enabled while DEBUG is false.",
                hint="Unset CODEX_PREVIEW_ENABLED outside local development.",
                id="django_codex_preview.E001",
            )
        ]
    return []
