---
name: clarify-requirements
description: Clarify requirements to at least 95% confidence before proceeding. Use for requirements capture, bug reports and investigation, issue refinement or planning, specifications, implementation, and any instruction to do work after a discussion, even when the user does not explicitly ask for questions.
---

# Clarify requirements before proceeding

Apply this rule in every project profile, including unconfigured projects, and
for work requested without an issue or explicit skill invocation.

1. Read the current request, prior discussion, any settled requirements, and
   relevant repository evidence. Carry forward settled answers; do not make the
   user repeat them when switching skills or moving from investigation to work
   already covered by the same established scope.
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
4. While answers are pending, continue useful read-only investigation of code,
   logs, documentation, and existing issues. Hold edits, implementation, issue
   creation or updates, and other mutations. Do not treat silence, elapsed time,
   or an unanswered question as an answer.
5. At 95% confidence or above, proceed without asking the user to confirm a
   requirements summary. Briefly state the understood scope, assumptions, or
   remaining non-blocking unknowns when that helps the user follow the work, but
   do not turn the summary into an approval gate. A clear initial instruction can
   itself provide enough information to reach the threshold.
6. Carry the established requirements throughout the work. Reopen clarification
   only for a material scope change or newly discovered ambiguity that lowers
   confidence below 95%. Routine implementation choices and transitions between
   skills do not restart the check.

For bug work, distinguish observed behavior, expected behavior, and whether the
requested deliverable is capture, diagnosis, or a fix. An unknown reproduction
or root cause can remain explicitly unknown in a sufficiently clear investigation
task; do not invent evidence or demand a solution before investigation. For
existing project specifications, distinguish observed behavior from intended
behavior.

Keep the summary proportional to the task; a small change can use a sentence.
Reaching the confidence threshold does not authorize unrelated actions or replace
any separate artifact preview or action approval required by the selected workflow.
