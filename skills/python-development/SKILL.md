---
name: python-development
description: Apply pragmatic Python implementation and review guidance. Use for Python applications, libraries, command-line tools, scripts, packaging, typing, logging, dependency management, and tests outside or alongside Django.
---

# Develop with Python

1. Load policy and inspect supported Python versions, dependency manager,
   `pyproject.toml`, package layout, typing level, linting, and test conventions.
2. Prefer clear conventional Python, small obvious abstractions, useful types at
   public or error-prone boundaries, and logging appropriate to the application.
3. Reuse existing dependency and environment tooling. Do not mix package managers
   or add a dependency for functionality the standard library handles clearly.
4. Keep simple utilities simple. Introduce layers or frameworks only when current
   complexity and repeated behavior justify them.
5. Add proportionate tests for meaningful logic and bug regressions. Run focused
   tests, configured lint/type checks, and canonical validation as policy requires.
6. Preserve compatibility with declared Python versions and avoid relying on the
   machine's incidental global environment.

