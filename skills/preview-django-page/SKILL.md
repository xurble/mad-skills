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
2. Otherwise use the helper in `resources/mad_skills_django_preview`. Check whether
   the project already exposes it. If not, explain the following minimal,
   development-only integration and obtain approval before editing the project:

   ```python
   # development settings
   MAD_SKILLS_PREVIEW_ENABLED = os.environ.get("MAD_SKILLS_PREVIEW_ENABLED") == "1"
   if MAD_SKILLS_PREVIEW_ENABLED:
       INSTALLED_APPS = [*INSTALLED_APPS, "mad_skills_django_preview"]

   # root URL configuration
   if getattr(settings, "MAD_SKILLS_PREVIEW_ENABLED", False):
       urlpatterns += [
           path("__mad_skills_preview__/", include("mad_skills_django_preview.urls")),
       ]
   ```

   Keep this resource off the project's normal dependency path. Add this
   skill's `resources` directory to `PYTHONPATH` only for the preview server.
3. Generate a fresh token with at least 32 random bytes and keep it outside the
   repository. Start the existing development server on `127.0.0.1` with
   `MAD_SKILLS_PREVIEW_ENABLED=1`, `MAD_SKILLS_PREVIEW_TOKEN=<token>`, and the resource
   directory prepended to `PYTHONPATH`. Never bind a preview server to a network
   interface. Confirm Django's system checks pass before continuing.
4. POST `application/json` to `__mad_skills_preview__/create/` from loopback with
   the token in `X-Mad-Skills-Preview-Token`. Supply a project-relative template name,
   bounded JSON `context`, optional `mode: "fragment"`, and an optional `persona`.
   A persona may contain `username`, `display_name`, `email`, `first_name`,
   `last_name`, `is_staff`, `is_superuser`, and a list of `permissions`.
5. Open the returned preview URL with the environment's available browser
   tooling. Check the representative page at useful viewport sizes, confirm
   expected static assets load, inspect browser-visible failures, and iterate on
   the template or inert context.
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
