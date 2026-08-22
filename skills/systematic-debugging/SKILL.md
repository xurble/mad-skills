---
name: systematic-debugging
description: Diagnose failures from reproducible evidence to root cause before changing code. Use for bugs, failing tests, crashes, incorrect behavior, integration failures, performance regressions, or intermittent problems that need investigation.
---

# Debug systematically

1. Load effective policy; passive use in an unconfigured repository assumes
   `light` without prompting.
2. Restate the observed failure and separate facts from assumptions.
3. Reproduce where practical. Capture the exact command, environment, output,
   logs, stack trace, failing test, or observable behavior.
4. Locate the failing boundary by narrowing inputs, layers, state, and timing.
5. Form a small set of falsifiable hypotheses and test them one at a time. Do not
   make random speculative patches.
6. Identify the root cause or explicitly report why evidence is insufficient.
7. If the user asked for a fix, make the smallest appropriate change, add useful
   regression coverage, and verify the original failure plus nearby behavior.
8. If not asked to fix, stop after diagnosis. If work remains, offer `open-bug`
   so evidence persists in GitHub.

