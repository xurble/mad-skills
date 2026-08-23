# Decision log

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
