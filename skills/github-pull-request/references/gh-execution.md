# Codex GitHub command execution

In Codex, run every `gh` command, and every `mad-skills` command that reaches
GitHub, outside the sandbox with escalation from the outset. This applies to
read and write commands. Keep each workflow's authentication, authorization,
target validation, and stopping rules in that workflow.
