---
name: django-development
description: Apply pragmatic Django-specific implementation and review guidance. Use for Django models, views, forms, admin, authentication, permissions, migrations, management commands, settings, templates, APIs, and tests.
---

# Develop with Django

1. Load project policy and read Django-specific repository guidance. Inspect the
   installed Django version, app boundaries, settings layout, URL patterns,
   dependency tooling, and test style before choosing an approach.
2. Prefer Django-native facilities where they fit: ORM, forms, migrations, admin,
   authentication/permissions, management commands, settings, and test tools.
3. Reuse existing architectural patterns. Keep substantial business logic out of
   views and admin callbacks, but do not create a service layer for trivial logic.
4. Treat schema and data migrations explicitly. Inspect generated operations,
   data volume, reversibility, deployment ordering, and compatibility. High-risk
   migrations use rigorous workflow regardless of profile.
5. Test permissions, validation, important business behavior, and regression
   paths proportionately. Run the project's configured commands.
6. Do not force DRF, Django Ninja, repositories, services, or another architecture
   the project has not chosen.

