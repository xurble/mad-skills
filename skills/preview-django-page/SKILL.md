---
name: preview-django-page
description: Preview changed Django templates and fragments through the project's local rendering stack and verify them visually in the browser.
---

# Preview a Django page

Use this workflow after changing a Django template or when the user asks to
preview Django-rendered HTML.

1. Inspect the Django version, settings modules, template engines, root URL
   configuration, static-file setup, development command, and existing preview
   support. Prefer a real application URL when it works locally without creating
   accounts, database records, permissions, or other fabricated state.
2. Otherwise use the helper in `resources/django_codex_preview`. Check whether
   the project already exposes it. If not, explain the following minimal,
   development-only integration and obtain approval before editing the project:

   ```python
   # development settings
   CODEX_PREVIEW_ENABLED = os.environ.get("CODEX_PREVIEW_ENABLED") == "1"
   if CODEX_PREVIEW_ENABLED:
       INSTALLED_APPS = [*INSTALLED_APPS, "django_codex_preview"]

   # root URL configuration
   if getattr(settings, "CODEX_PREVIEW_ENABLED", False):
       urlpatterns += [
           path("__codex_preview__/", include("django_codex_preview.urls")),
       ]
   ```

   Keep this resource off the project's normal dependency path. Add this
   skill's `resources` directory to `PYTHONPATH` only for the preview server.
3. Generate a fresh token with at least 32 random bytes and keep it outside the
   repository. Start the existing development server on `127.0.0.1` with
   `CODEX_PREVIEW_ENABLED=1`, `CODEX_PREVIEW_TOKEN=<token>`, and the resource
   directory prepended to `PYTHONPATH`. Never bind a preview server to a network
   interface. Confirm Django's system checks pass before continuing.
4. POST `application/json` to `__codex_preview__/create/` from loopback with the
   token in `X-Codex-Preview-Token`. Supply a project-relative template name,
   bounded JSON `context`, optional `mode: "fragment"`, and an optional `persona`.
   A persona may contain `username`, `display_name`, `email`, `first_name`,
   `last_name`, `is_staff`, `is_superuser`, and a list of `permissions`.
5. Open the returned preview URL in Codex's browser. Check the representative
   page at useful viewport sizes, confirm expected static assets load, inspect
   browser-visible failures, and iterate on the template or inert context.
6. Stop any server started for the preview. Preview specifications are held only
   in that server's bounded memory and expire within five minutes.

The helper renders templates with Django's request-aware template backend, so
ordinary request/response middleware and context processors remain active. It
does not call the page's view, query models, establish sessions, or allow form
submission. A virtual persona is only an in-memory presentation object.

This is a development convenience, not a sandbox. Trust remains in the
repository and its installed dependencies, including middleware, context
processors, template loaders, templates, custom tags, and static assets. Do not
preview an untrusted project or use context that contains secrets.
