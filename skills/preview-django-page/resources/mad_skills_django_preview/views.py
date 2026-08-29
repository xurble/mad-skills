from __future__ import annotations

import ipaddress
import json
import os
import secrets
from importlib.resources import files
from pathlib import Path
from typing import Any

from django.apps import apps
from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.template import TemplateDoesNotExist, engines
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .preview import InvalidPreview, PreviewSpec, PreviewUser, parse_payload
from .store import preview_store

MAX_REQUEST_BYTES = 65_536
TOKEN_ENVIRONMENT_VARIABLE = "MAD_SKILLS_PREVIEW_TOKEN"
TOKEN_HEADER = "X-Mad-Skills-Preview-Token"


class RequestTooLarge(InvalidPreview):
    """The control request exceeds the helper's fixed body limit."""


def _not_found() -> None:
    raise Http404


def _require_available(request: HttpRequest) -> None:
    if not settings.DEBUG or getattr(settings, "MAD_SKILLS_PREVIEW_ENABLED", False) is not True:
        _not_found()
    try:
        peer = ipaddress.ip_address(request.META.get("REMOTE_ADDR", ""))
    except ValueError:
        _not_found()
    if not peer.is_loopback or _has_authenticated_session(request):
        _not_found()


def _has_authenticated_session(request: HttpRequest) -> bool:
    user = getattr(request, "user", None)
    if user is not None and bool(getattr(user, "is_authenticated", False)):
        return True
    session = getattr(request, "session", None)
    return session is not None and SESSION_KEY in session


def _require_capability(request: HttpRequest) -> None:
    expected = os.environ.get(TOKEN_ENVIRONMENT_VARIABLE, "")
    supplied = request.headers.get(TOKEN_HEADER, "")
    if len(expected) < 32 or not supplied or not secrets.compare_digest(expected, supplied):
        _not_found()


def _security_headers(response: HttpResponse) -> HttpResponse:
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "form-action 'none'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Robots-Tag"] = "noindex"
    return response


def _invalid(message: str, *, status: int = 400) -> JsonResponse:
    return _security_headers(JsonResponse({"error": message}, status=status))


def _decode_payload(request: HttpRequest) -> Any:
    if request.content_type != "application/json":
        raise InvalidPreview("Content-Type must be application/json.")
    content_length = request.META.get("CONTENT_LENGTH")
    if content_length:
        try:
            parsed_content_length = int(content_length)
        except ValueError as exc:
            raise InvalidPreview("Content-Length is invalid.") from exc
        if parsed_content_length > MAX_REQUEST_BYTES:
            raise RequestTooLarge("Request body is too large.")
    body = request.body
    if len(body) > MAX_REQUEST_BYTES:
        raise RequestTooLarge("Request body is too large.")

    def reject_constant(value: str) -> None:
        raise InvalidPreview(f"Non-finite JSON number {value!r} is not supported.")

    try:
        return json.loads(body.decode("utf-8"), parse_constant=reject_constant)
    except RecursionError as exc:
        raise InvalidPreview("Request JSON nesting is too deep.") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidPreview("Request body must contain valid UTF-8 JSON.") from exc


def _approved_template_roots() -> tuple[Path, ...]:
    configured = getattr(settings, "MAD_SKILLS_PREVIEW_TEMPLATE_ROOTS", None)
    if configured is not None:
        if isinstance(configured, (str, bytes)):
            return ()
        return tuple(Path(root).expanduser().resolve() for root in configured)

    base_dir = Path(settings.BASE_DIR).resolve()
    roots: set[Path] = set()
    for backend in settings.TEMPLATES:
        for root in backend.get("DIRS", []):
            candidate = Path(root).expanduser().resolve()
            if candidate.is_relative_to(base_dir):
                roots.add(candidate)
    for app_config in apps.get_app_configs():
        app_path = Path(app_config.path).resolve()
        candidate = app_path / "templates"
        if app_path.is_relative_to(base_dir) and candidate.is_dir():
            roots.add(candidate.resolve())
    return tuple(sorted(roots))


def _validate_template_origin(template_name: str) -> None:
    try:
        template = get_template(template_name)
    except TemplateDoesNotExist as exc:
        raise InvalidPreview("Template could not be found.") from exc
    origin_name = getattr(getattr(template, "origin", None), "name", None)
    if not origin_name:
        raise InvalidPreview("Template loader did not provide an approved filesystem origin.")
    origin = Path(origin_name).resolve()
    if not any(origin.is_relative_to(root) for root in _approved_template_roots()):
        raise InvalidPreview("Template origin is outside the approved project roots.")


@csrf_exempt
def create_preview(request: HttpRequest) -> HttpResponse:
    _require_available(request)
    if request.method != "POST":
        _not_found()
    _require_capability(request)
    try:
        spec = parse_payload(_decode_payload(request))
        _validate_template_origin(spec.template_name)
    except InvalidPreview as exc:
        status = 413 if isinstance(exc, RequestTooLarge) else 400
        return _invalid(str(exc), status=status)
    preview_id = preview_store.create(spec)
    preview_url = request.build_absolute_uri(
        reverse("mad_skills_django_preview:render", kwargs={"preview_id": preview_id})
    )
    return _security_headers(
        JsonResponse(
            {
                "expires_in": preview_store.ttl_seconds,
                "id": preview_id,
                "url": preview_url,
            },
            status=201,
        )
    )


def render_preview(request: HttpRequest, preview_id: str) -> HttpResponse:
    _require_available(request)
    if request.method != "GET":
        _not_found()
    spec = preview_store.get(preview_id)
    if spec is None:
        _not_found()
    if spec.persona is not None:
        request.user = PreviewUser(spec.persona)
    response = _template_response(request, spec)
    return _security_headers(response)


def _template_response(request: HttpRequest, spec: PreviewSpec) -> TemplateResponse:
    if not spec.fragment:
        return TemplateResponse(request, spec.template_name, spec.context)
    wrapper_source = (
        files("mad_skills_django_preview")
        .joinpath("templates/mad_skills_django_preview/fragment.html")
        .read_text(encoding="utf-8")
    )
    wrapper = engines["django"].from_string(wrapper_source)
    context = {**spec.context, "mad_skills_preview_template": spec.template_name}
    return TemplateResponse(request, wrapper, context)
