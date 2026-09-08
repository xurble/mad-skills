---
name: clarify-requirements
description: Clarify requirements to at least 95% confidence and obtain confirmation before proceeding. Use for requirements capture, bug reports and investigation, issue refinement or planning, specifications, implementation, and any instruction to do work after a discussion, even when the user does not explicitly ask for questions.
---

# Clarify requirements before proceeding

Apply this rule in every project profile, including unconfigured projects, and
for work requested without an issue or explicit skill invocation.

For an explicitly enabled nightly run or approved setup trial, first apply
[standing authorization](../nightly-implement/references/authorization.md).
Trusted project/issue-scoped authorization satisfies the routine confirmation
gate below: still assess confidence and record the summary, but do not ask again.
New material ambiguity stops dependent work with the nightly blocked handoff,
not an unattended question. Outside this mode, the interactive steps below apply.

1. Read the current request, prior discussion, any confirmed requirements, and
   relevant repository evidence. Carry forward settled answers; do not make the
   user repeat them when switching skills or moving from investigation to work
   already covered by the same confirmed scope.
2. Assess whether you are at least 95% confident about the intended outcome,
   scope, constraints, and observable success criteria. This is a judgment about
   understanding the requirements, not a measured probability or certainty about
   the implementation or a bug's root cause. A material unresolved requirement
   keeps confidence below the threshold.
3. Below 95%, proactively ask focused questions that resolve the most consequential
   ambiguity. Ask in small, manageable groups, offer concrete alternatives when
   useful, and use each answer to decide whether more questions are needed. Do
   not ask the user for facts that repository evidence can settle. There is no
   minimum question count when the requirements are already clear.
4. While answers or confirmation are pending, continue useful read-only
   investigation of code, logs, documentation, and existing issues. Hold edits,
   implementation, issue creation or updates, and other mutations. Do not treat
   silence, elapsed time, or an unanswered question as an answer or confirmation.
5. At 95% confidence or above, present a concise requirements summary covering the
   intended outcome, scope, relevant constraints, success criteria, and any
   remaining non-blocking unknowns. Ask the user to explicitly confirm it and
   wait before proceeding. Do this even when no clarification questions were
   needed. The initial instruction to do the work does not itself confirm a
   summary that has not yet been presented.
6. After confirmation, proceed within that scope and reuse the confirmation
   throughout the work. A response such as “confirm, proceed” to the summary
   satisfies this step. Reopen clarification and confirmation only for a material
   scope change or newly discovered ambiguity affecting the requirements. Routine
   implementation choices and transitions between skills do not restart the gate.

For bug work, distinguish observed behavior, expected behavior, and whether the
requested deliverable is capture, diagnosis, or a fix. An unknown reproduction
or root cause can remain explicitly unknown in a confirmed investigation task;
do not invent evidence or demand a solution before investigation. For existing
project specifications, distinguish observed behavior from intended behavior.

Keep the summary proportional to the task; a small change can use a sentence.
Requirements confirmation does not authorize unrelated actions or replace any
separate artifact preview or action approval required by the selected workflow.
