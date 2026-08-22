---
name: specify-existing-project
description: Derive a current-state behavioral and product specification from an existing implementation when specifications are missing, incomplete, or stale. Use when asked to reverse-engineer requirements, document an inherited project as built, reconstruct intended behavior from code and tests, or produce a specification from implementation; always surface unclear intent as explicit assumptions for user clarification.
---

# Specify an existing project

Treat the implementation as evidence of behavior, not unquestionable evidence of
intent. Do not turn every accident, bug, dead path, or historical compromise into
a requirement.

## Establish scope

1. Load `mad-skills context --format json`; passive use without configuration
   assumes `light`.
2. Read `AGENTS.md`, existing documentation, decisions, issues, and repository
   structure. Use `$understand-project` first when the repository is unfamiliar.
3. Confirm the requested specification scope: whole product, subsystem, workflow,
   API, or migration. For a large repository, propose a bounded first scope rather
   than claiming exhaustive coverage.
4. Inspect repository status and remain read-only during investigation. Do not
   rewrite documentation until the draft and assumptions have been reviewed.

## Reconstruct behavior

1. Trace externally observable behavior through entry points, UI, routes, APIs,
   commands, jobs, persistence, integrations, and error paths.
2. Read tests as behavioral evidence, especially acceptance, integration, and
   regression tests. Run safe existing checks only when they materially resolve an
   uncertainty; do not mutate real data or call production services.
3. Build an evidence hierarchy:
   - explicit user clarification and maintained decisions;
   - executable acceptance or integration behavior;
   - public interfaces, schemas, UI states, and persisted invariants;
   - implementation details and unit tests;
   - comments, names, and weak inference.
4. Record contradictions between documentation, tests, and code. Do not silently
   choose whichever source is convenient.
5. Separate each conclusion into one of:
   - **observed behavior** — directly supported by evidence;
   - **inferred intention** — likely, but not conclusive;
   - **unknown** — insufficient or contradictory evidence;
   - **suspected defect or dead behavior** — should not be canonized without a decision.

## Draft the specification

Produce a traceable current-state draft containing, where relevant:

- scope, purpose, actors, and terminology;
- user-visible workflows and functional requirements with stable identifiers;
- inputs, outputs, interfaces, data rules, states, permissions, and invariants;
- validation, error handling, edge cases, and recovery behavior;
- integrations, compatibility constraints, and meaningful non-functional behavior;
- explicit non-goals and excluded areas;
- evidence references to paths, symbols, tests, routes, schemas, or observed output;
- contradictions, suspected defects, and coverage gaps;
- an **Assumptions requiring clarification** section.

Describe what the system currently does separately from proposed improvements. Do
not introduce desired future behavior unless the user asks for a target-state spec.

## Raise assumptions for clarification

For every material point where intention is not completely clear, create an entry:

```text
A-001 — Short assumption
Provisional interpretation: What the draft currently assumes.
Evidence: What supports or contradicts it.
Confidence: high | medium | low
Impact if wrong: Which requirements, data, users, or interfaces change.
Question: One concrete question the user can answer.
```

Keep assumptions specific, non-overlapping, and decision-relevant. Do not ask the
user to clarify facts that repository evidence can settle. Order the list by impact,
then ask the questions in manageable groups rather than presenting a wall of minor
uncertainties.

## Finalize

1. Present the draft and numbered assumptions before writing a repository document.
2. Incorporate user clarifications, recording which assumptions were confirmed,
   corrected, or intentionally left unresolved.
3. If unresolved assumptions remain, preserve them visibly in the specification;
   never convert them silently into facts.
4. Write to the repository's established specification location after approval, or
   propose `docs/specification.md` when no convention exists.
5. Report the evidence inspected, checks run, remaining gaps, and areas deliberately
   excluded from the specification.

