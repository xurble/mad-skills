from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

MAX_COLLECTION_ITEMS = 100
MAX_CONTEXT_ITEMS = 1_000
MAX_DEPTH = 8
MAX_STRING_LENGTH = 4_096
MAX_INTEGER = 2**63 - 1
RESERVED_CONTEXT_KEYS = {"csrf_token", "perms", "request", "user"}
PERSONA_FIELDS = {
    "display_name",
    "email",
    "first_name",
    "is_staff",
    "is_superuser",
    "last_name",
    "permissions",
    "username",
}


class InvalidPreview(ValueError):
    """The requested preview cannot be represented safely."""


@dataclass(frozen=True)
class Persona:
    username: str = "preview-user"
    display_name: str = "Preview User"
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    is_staff: bool = False
    is_superuser: bool = False
    permissions: frozenset[str] = frozenset()


@dataclass(frozen=True)
class PreviewSpec:
    template_name: str
    context: dict[str, Any]
    fragment: bool
    persona: Persona | None


class PreviewUser:
    def __init__(self, persona: Persona) -> None:
        self.username = persona.username
        self.display_name = persona.display_name
        self.email = persona.email
        self.first_name = persona.first_name
        self.last_name = persona.last_name
        self.is_staff = persona.is_staff
        self.is_superuser = persona.is_superuser
        self._permissions = persona.permissions
        self.id = None
        self.pk = None

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return True

    def get_username(self) -> str:
        return self.username

    def get_full_name(self) -> str:
        return " ".join(part for part in (self.first_name, self.last_name) if part) or self.display_name

    def get_short_name(self) -> str:
        return self.first_name or self.display_name or self.username

    def get_all_permissions(self, obj: object | None = None) -> set[str]:
        return set(self._permissions)

    def has_perm(self, perm: str, obj: object | None = None) -> bool:
        return self.is_superuser or perm in self._permissions

    def has_perms(self, perm_list: list[str], obj: object | None = None) -> bool:
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label: str) -> bool:
        prefix = f"{app_label}."
        return self.is_superuser or any(perm.startswith(prefix) for perm in self._permissions)

    def __str__(self) -> str:
        return self.display_name or self.username


def parse_payload(payload: Any) -> PreviewSpec:
    if not isinstance(payload, dict):
        raise InvalidPreview("The request body must be a JSON object.")
    unexpected = set(payload) - {"context", "mode", "persona", "template"}
    if unexpected:
        raise InvalidPreview("The request contains unsupported fields.")

    template_name = payload.get("template")
    validate_template_name(template_name)

    context = payload.get("context", {})
    if not isinstance(context, dict):
        raise InvalidPreview("Context must be a JSON object.")
    if RESERVED_CONTEXT_KEYS.intersection(context):
        raise InvalidPreview("Context contains request-managed keys.")
    _validate_json_value(context, depth=0, counter=[0])

    mode = payload.get("mode", "page")
    if mode not in {"page", "fragment"}:
        raise InvalidPreview("Mode must be 'page' or 'fragment'.")

    return PreviewSpec(
        template_name=template_name,
        context=context,
        fragment=mode == "fragment",
        persona=_parse_persona(payload.get("persona")),
    )


def validate_template_name(value: Any) -> None:
    if not isinstance(value, str) or not value or len(value) > 255:
        raise InvalidPreview("Template must be a non-empty string of at most 255 characters.")
    normalized = value.replace("\\", "/")
    parts = normalized.split("/")
    if "\x00" in value or normalized.startswith("/") or any(part in {"", ".", ".."} for part in parts):
        raise InvalidPreview("Template must be a relative name without traversal.")
    if len(parts[0]) == 2 and parts[0][1] == ":":
        raise InvalidPreview("Template must not be an absolute path.")


def _parse_persona(value: Any) -> Persona | None:
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) - PERSONA_FIELDS:
        raise InvalidPreview("Persona must contain only supported fields.")
    for field in ("username", "display_name", "email", "first_name", "last_name"):
        if field in value and (not isinstance(value[field], str) or len(value[field]) > 254):
            raise InvalidPreview(f"Persona {field} must be a short string.")
    for field in ("is_staff", "is_superuser"):
        if field in value and not isinstance(value[field], bool):
            raise InvalidPreview(f"Persona {field} must be a boolean.")
    permissions = value.get("permissions", [])
    if (
        not isinstance(permissions, list)
        or len(permissions) > 50
        or any(not isinstance(item, str) or not item or len(item) > 150 for item in permissions)
    ):
        raise InvalidPreview("Persona permissions must be a short list of permission strings.")
    return Persona(
        username=value.get("username", "preview-user"),
        display_name=value.get("display_name", "Preview User"),
        email=value.get("email", ""),
        first_name=value.get("first_name", ""),
        last_name=value.get("last_name", ""),
        is_staff=value.get("is_staff", False),
        is_superuser=value.get("is_superuser", False),
        permissions=frozenset(permissions),
    )


def _validate_json_value(value: Any, *, depth: int, counter: list[int]) -> None:
    counter[0] += 1
    if counter[0] > MAX_CONTEXT_ITEMS:
        raise InvalidPreview("Context contains too many values.")
    if depth > MAX_DEPTH:
        raise InvalidPreview("Context nesting is too deep.")
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, str):
        if len(value) > MAX_STRING_LENGTH:
            raise InvalidPreview("Context contains an oversized string.")
        return
    if isinstance(value, int):
        if abs(value) > MAX_INTEGER:
            raise InvalidPreview("Context contains an oversized integer.")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InvalidPreview("Context contains a non-finite number.")
        return
    if isinstance(value, list):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise InvalidPreview("Context contains an oversized list.")
        for item in value:
            _validate_json_value(item, depth=depth + 1, counter=counter)
        return
    if isinstance(value, dict):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise InvalidPreview("Context contains an oversized object.")
        for key, item in value.items():
            if not isinstance(key, str) or len(key) > MAX_STRING_LENGTH:
                raise InvalidPreview("Context object keys must be short strings.")
            if key.startswith("$") or key.startswith("__"):
                raise InvalidPreview("Context contains a prohibited protocol key.")
            _validate_json_value(item, depth=depth + 1, counter=counter)
        return
    raise InvalidPreview("Context contains an unsupported value type.")
