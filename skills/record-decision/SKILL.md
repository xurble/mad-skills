---
name: record-decision
description: Record a significant project decision and rationale in the configured decision log. Use when an architectural or long-lived choice has meaningful alternatives, reversal cost, compatibility constraints, or context future maintainers would otherwise lose.
---

# Record a decision

1. Load effective policy. Offer `mad-skills init` when project configuration is
   absent. Locate `decisions.log`; if none is configured, propose
   `docs/decisions.md` and ask before creating it.
2. Record only a real decision: architecture, framework, persistence, sync,
   deployment, compatibility, rejected alternative, or consequential data model.
   Do not log routine implementation details.
3. Confirm the decision is settled. Distinguish the chosen direction from open
   questions and avoid reconstructing rationale without evidence.
4. Read the existing log to avoid duplicates and preserve its format. Consult
   `<resolved.toolkit_root>/templates/decision-entry.md` when starting a log.
5. Add the date, decision, context, rationale, alternatives, and consequences or
   constraints. Keep the entry concise enough to remain useful.
6. Show the proposed entry when rationale or wording requires judgment; a direct,
   fully specified request authorizes writing it.
