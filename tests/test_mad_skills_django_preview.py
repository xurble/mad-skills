from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pytest

RESOURCE_ROOT = Path(__file__).parents[1] / "skills/preview-django-page/resources"
sys.path.insert(0, str(RESOURCE_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.django_preview_project.settings")

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.staticfiles.handlers import StaticFilesHandler  # noqa: E402
from django.core import checks  # noqa: E402
from django.core.handlers.wsgi import WSGIHandler  # noqa: E402
from django.test import Client, override_settings  # noqa: E402
from mad_skills_django_preview import views  # noqa: E402
from mad_skills_django_preview.preview import PreviewUser, parse_payload  # noqa: E402
from mad_skills_django_preview.store import PreviewStore, preview_store  # noqa: E402

TOKEN = "test-token-with-at-least-thirty-two-characters"
CREATE_PATH = "/__mad_skills_preview__/create/"


@pytest.fixture(autouse=True)
def isolated_preview_store(monkeypatch):
    preview_store.clear()
    monkeypatch.setenv("MAD_SKILLS_PREVIEW_TOKEN", TOKEN)
    yield
    preview_store.clear()


def create_preview(client: Client, payload: dict | None = None, **request_options):
    body = payload or {
        "template": "page.html",
        "context": {"title": "Preview title", "items": ["one", "two"]},
    }
    options = {
        "content_type": "application/json",
        "headers": {"X-Mad-Skills-Preview-Token": TOKEN},
    }
    options.update(request_options)
    return client.post(CREATE_PATH, data=json.dumps(body), **options)


def preview_path(response) -> str:
    return urlsplit(response.json()["url"]).path


def call_wsgi(application, path: str) -> tuple[str, dict[str, str], bytes]:
    environ = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": path,
        "SERVER_NAME": "testserver",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.input": __import__("io").BytesIO(),
        "wsgi.url_scheme": "http",
        "wsgi.version": (1, 0),
        "wsgi.errors": sys.stderr,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    result = application(environ, start_response)
    try:
        body = b"".join(result)
    finally:
        if hasattr(result, "close"):
            result.close()
    return captured["status"], captured["headers"], body


def test_inheriting_page_uses_context_middleware_processors_and_static_assets():
    client = Client()
    created = create_preview(client)

    assert created.status_code == 201
    rendered = client.get(preview_path(created))

    assert rendered.status_code == 200
    content = rendered.content.decode()
    assert "<title>Preview title</title>" in content
    assert "<li>one</li><li>two</li>" in content.replace("\n", "").replace("  ", "")
    assert "context-processor-active" in content
    assert "request-middleware-active" in content
    assert 'href="/static/preview.css"' in content
    assert rendered.headers["X-Sample-Middleware"] == "response-middleware-active"

    status, _, static_content = call_wsgi(StaticFilesHandler(WSGIHandler()), "/static/preview.css")
    assert status.startswith("200")
    assert b"rgb(20, 30, 40)" in static_content


def test_fragment_uses_bundled_wrapper_without_project_wrapper():
    response = create_preview(
        Client(),
        {
            "template": "card.html",
            "mode": "fragment",
            "context": {"heading": "Card heading", "body": "Card body"},
        },
    )

    rendered = Client().get(preview_path(response))

    assert rendered.status_code == 200
    assert b"data-mad-skills-preview-fragment" in rendered.content
    assert b'<article class="card"><h2>Card heading</h2><p>Card body</p></article>' in rendered.content


@pytest.mark.parametrize(
    ("overrides", "expected_status"),
    [
        ({"DEBUG": False, "MAD_SKILLS_PREVIEW_ENABLED": True}, 404),
        ({"DEBUG": True, "MAD_SKILLS_PREVIEW_ENABLED": False}, 404),
        ({"DEBUG": True, "MAD_SKILLS_PREVIEW_ENABLED": "true"}, 404),
    ],
)
def test_enablement_gates_repeat_inside_views(overrides, expected_status):
    with override_settings(**overrides):
        assert create_preview(Client()).status_code == expected_status


def test_enabled_with_debug_false_reports_critical_system_check():
    with override_settings(DEBUG=False, MAD_SKILLS_PREVIEW_ENABLED=True):
        findings = checks.run_checks()

    finding = next(item for item in findings if item.id == "mad_skills_django_preview.E001")
    assert finding.level == checks.CRITICAL


def test_loopback_is_required_for_create_and_render():
    client = Client()
    created = create_preview(client)

    assert create_preview(Client(), REMOTE_ADDR="203.0.113.10").status_code == 404
    assert client.get(preview_path(created), REMOTE_ADDR="203.0.113.10").status_code == 404


def test_creation_requires_json_and_correct_capability_without_cors():
    client = Client()

    missing = client.post(CREATE_PATH, data="{}", content_type="application/json")
    wrong = client.post(
        CREATE_PATH,
        data="{}",
        content_type="application/json",
        headers={"X-Mad-Skills-Preview-Token": "wrong"},
    )
    non_json = client.post(
        CREATE_PATH,
        data="template=page.html",
        content_type="application/x-www-form-urlencoded",
        headers={"X-Mad-Skills-Preview-Token": TOKEN},
    )
    options = client.options(CREATE_PATH, headers={"Origin": "https://example.test"})

    assert missing.status_code == 404
    assert wrong.status_code == 404
    assert non_json.status_code == 400
    assert options.status_code == 404
    assert "Access-Control-Allow-Origin" not in options.headers


def test_unknown_and_expired_preview_ids_return_404(monkeypatch):
    now = [10.0]
    expiring_store = PreviewStore(ttl_seconds=1, clock=lambda: now[0])
    monkeypatch.setattr(views, "preview_store", expiring_store)
    created = create_preview(Client())
    path = preview_path(created)

    assert Client().get("/__mad_skills_preview__/p/unknown/").status_code == 404
    now[0] = 11.0
    assert Client().get(path).status_code == 404
    assert len(expiring_store) == 0


def test_authenticated_session_is_refused_without_mutation():
    created = create_preview(Client())
    authenticated = Client()
    session = authenticated.session
    session["preview_authenticated"] = True
    session["unchanged"] = "sentinel"
    session.save()
    authenticated.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
    cookie_before = authenticated.cookies[settings.SESSION_COOKIE_NAME].value

    response = authenticated.get(preview_path(created))

    assert response.status_code == 404
    assert authenticated.session["preview_authenticated"] is True
    assert authenticated.session["unchanged"] == "sentinel"
    assert authenticated.cookies[settings.SESSION_COOKIE_NAME].value == cookie_before


def test_virtual_persona_changes_presentation_without_session_or_user_model():
    client = Client()
    created = create_preview(
        client,
        {
            "template": "page.html",
            "context": {"title": "Persona", "items": []},
            "persona": {
                "username": "virtual",
                "display_name": "Virtual Reviewer",
                "is_staff": True,
                "permissions": ["shop.view_report"],
            },
        },
    )

    rendered = client.get(preview_path(created))

    assert rendered.status_code == 200
    assert b"Virtual Reviewer" in rendered.content
    assert b"staff-presentation" in rendered.content
    assert settings.SESSION_COOKIE_NAME not in client.cookies
    assert "django.contrib.auth" not in settings.INSTALLED_APPS

    spec = parse_payload(
        {"template": "page.html", "persona": {"permissions": ["shop.view_report"]}}
    )
    assert spec.persona is not None
    assert PreviewUser(spec.persona).has_perm("shop.view_report")


@pytest.mark.parametrize(
    "payload",
    [
        {"template": "../page.html", "context": {}},
        {"template": "/tmp/page.html", "context": {}},
        {"template": "page.html\x00", "context": {}},
        {"template": "page.html", "context": {"request": {}}},
        {"template": "page.html", "context": {"$type": "model"}},
        {"template": "page.html", "context": {"value": "x" * 4_097}},
        {"template": "page.html", "context": {"items": list(range(101))}},
        {"template": "page.html", "context": {"nested": [[[[[[[[[[]]]]]]]]]]}},
        {"template": "page.html", "context": {}, "operation": "call"},
        {"template": "page.html", "context": {}, "persona": {"user_model": "auth.User"}},
    ],
)
def test_control_endpoint_rejects_prohibited_and_oversized_inputs(payload):
    assert create_preview(Client(), payload).status_code == 400


def test_control_endpoint_rejects_oversized_body_and_non_finite_json():
    client = Client()
    huge = json.dumps({"template": "page.html", "context": {"value": "x" * 70_000}})

    oversized = client.post(
        CREATE_PATH,
        data=huge,
        content_type="application/json",
        headers={"X-Mad-Skills-Preview-Token": TOKEN},
    )
    non_finite = client.post(
        CREATE_PATH,
        data='{"template":"page.html","context":{"value":NaN}}',
        content_type="application/json",
        headers={"X-Mad-Skills-Preview-Token": TOKEN},
    )

    assert oversized.status_code == 413
    assert non_finite.status_code == 400


def test_control_endpoint_rejects_invalid_content_length():
    response = Client().generic(
        "POST",
        CREATE_PATH,
        data=b"{}",
        content_type="application/json",
        CONTENT_LENGTH="invalid",
        HTTP_X_MAD_SKILLS_PREVIEW_TOKEN=TOKEN,
    )

    assert response.status_code == 400


def test_control_endpoint_rejects_json_beyond_decoder_recursion_limit():
    nesting = sys.getrecursionlimit() + 100
    nested_value = "[" * nesting + "0" + "]" * nesting
    body = '{"template":"page.html","context":{"nested":' + nested_value + "}}"

    response = Client().post(
        CREATE_PATH,
        data=body,
        content_type="application/json",
        headers={"X-Mad-Skills-Preview-Token": TOKEN},
    )

    assert response.status_code == 400
    assert response.json() == {"error": "Request JSON nesting is too deep."}


def test_template_origin_must_be_inside_approved_project_roots():
    response = create_preview(
        Client(),
        {"template": "mad_skills_django_preview/fragment.html", "context": {}},
    )

    assert response.status_code == 400
    assert response.json() == {"error": "Template origin is outside the approved project roots."}


def test_store_is_memory_only_bounded_and_uses_random_192_bit_ids():
    store = PreviewStore(max_previews=2)
    spec = parse_payload({"template": "page.html", "context": {}})

    first = store.create(spec)
    second = store.create(spec)
    third = store.create(spec)

    assert len(first) >= 32
    assert len({first, second, third}) == 3
    assert len(store) == 2
    assert store.get(first) is None
    assert PreviewStore().get(second) is None


def test_preview_security_headers_block_forms_caching_indexing_and_frames():
    created = create_preview(Client())
    rendered = Client().get(preview_path(created))

    for response in (created, rendered):
        assert response.headers["Cache-Control"] == "no-store"
        assert "form-action 'none'" in response.headers["Content-Security-Policy"]
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-Robots-Tag"] == "noindex"
        assert "Access-Control-Allow-Origin" not in response.headers


def test_preview_root_and_non_get_render_expose_nothing():
    created = create_preview(Client())

    assert Client().get("/__mad_skills_preview__/").status_code == 404
    assert Client().post(preview_path(created)).status_code == 404
