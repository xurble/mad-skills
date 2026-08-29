# Decision log

## 2026-08-29 — Bundle the Django preview helper inside its skill

**Decision:**

Ship `django_codex_preview` as a Python resource inside the
`preview-django-page` skill. Add the resource directory to `PYTHONPATH` only for
the local preview server; do not publish it or add it to the toolkit's runtime
package.

**Context:**

Django templates need the project's rendering stack for useful browser previews,
but consuming projects should not gain a production dependency or maintain a
preview view for every page. Installed skills are symlinked directly to this
checkout, so their resources already share the toolkit's update lifecycle.

**Rationale:**

A skill resource keeps the workflow and helper version together, remains
immediately available to installed consumers, and disappears from importability
when the preview server is not launched with the temporary path. A consuming
project needs only a small flag-gated URL integration while retaining its normal
settings, middleware, template loaders, context processors, and static serving.

**Alternatives considered:**

- Publish a separate development dependency. Rejected because it adds a second
  release and installation lifecycle for a personal source-of-truth toolkit.
- Put the helper in `src/mad_skills`. Rejected because it would make Django
  preview code part of the general CLI package and its ordinary import path.
- Add project-specific preview views or scenarios. Rejected because it repeats
  infrastructure for each consuming project and page.

**Consequences and constraints:**

- Preview server commands must prepend the skill's `resources` directory to
  `PYTHONPATH` and bind to loopback.
- Consuming projects must explicitly approve the small development URL and
  setting integration; the skill cannot modify it silently.
- The helper supports Django 5.2 and 6.x while those versions fit the toolkit's
  Python support, and tests resolve both through the development lock.
- The helper remains a trusted development tool, not a sandbox for malicious
  middleware, context processors, templates, tags, or dependencies.

## 2026-08-23 — Use pull requests as the rigorous delivery contract

**Decision:**

For rigorous non-trivial work, use a standalone, well-specified pull request as
the durable delivery contract and merge gate. An issue is optional and is linked
only when it drove the work. Open the pull request as a draft while fresh AI
review is pending, and mark it ready after the accepted review cycle completes.
The developer may explicitly override only the AI-review gate.

**Context:**

This toolkit serves primarily one-person projects. Requiring an issue for work
already specified and approved in conversation duplicated the change contract
without adding corresponding safety. The workflow still needs a durable record
of final scope and a visible indication that independent review is pending.

**Rationale:**

A standalone pull request keeps the accepted outcome, motivation, scope,
acceptance criteria, implementation, validation, and risks beside the exact diff
being merged. Draft state provides a lightweight, visible review gate without
requiring workflow orchestration. Issues remain useful as a backlog and retain
their normal closing relationship when they are the source of the work.

**Alternatives considered:**

- Require an issue for every rigorous change. Rejected because it duplicates an
  already accepted specification and adds ceremony to issue-less work.
- Start fresh AI review automatically when a draft pull request is created.
  Rejected because review should begin only after explicit user acceptance.
- Make AI review impossible to bypass. Rejected because the developer retains
  final authority in a personal toolkit; any override must be explicit and the
  skipped review must be disclosed.

**Consequences and constraints:**

- Rigorous pull requests must stand alone and not depend on chat or issue history.
- Existing issues are linked and closed only when they actually drove the work.
- A draft rigorous pull request represents pending fresh AI review.
- Material findings keep the pull request in draft and require another fresh
  review after remediation.
- An explicit override bypasses only the AI-review gate, not other required
  planning, verification, tests, or repository checks.
- The workflow must not automatically launch review or merge pull requests.
