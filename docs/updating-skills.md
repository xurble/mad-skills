# Update mad-skills

The checkout is the version and distribution mechanism:

```bash
cd /path/to/mad-skills
git pull
mad-skills validate
```

User-scope skill links and the editable uv tool environment point at this checkout,
so no reinstall is normally needed. Rerun `./scripts/install --target all` after
adding a new skill or repairing links; it is idempotent and stops on conflicts.

Before accepting an update:

```bash
uv run pytest
uv run ruff check .
mad-skills validate
```

Projects that truly need reproducible agent behavior may pin this repository to a
Git revision manually. V1 does not implement per-project version resolution or an
update command.

