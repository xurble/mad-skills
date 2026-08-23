from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mad_skills import __version__
from mad_skills.checker import check_project
from mad_skills.configuration import (
    dump_yaml,
    github_workflow_enabled,
    load_yaml,
    resolve_project,
    validate_project_data,
)
from mad_skills.errors import MadSkillsError
from mad_skills.github import (
    configure_repository,
    create_labels,
    mismatched_repository_settings,
    missing_labels,
)
from mad_skills.initialize import initialize_interactive
from mad_skills.installer import install, skill_directories
from mad_skills.paths import find_repo_root, find_toolkit_root
from mad_skills.validation import validate_toolkit


class MadSkillsArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        if "--check-command" in message and "expected one argument" in message:
            message = (
                "--check-command needs the project validation command as its value. "
                "For example: mad-skills init --check-command './scripts/check'"
            )
        super().error(message)


def build_parser() -> argparse.ArgumentParser:
    parser = MadSkillsArgumentParser(prog="mad-skills", description="Personal Agent Skills toolkit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="link shared skills into agent user scopes")
    install_parser.add_argument("--target", choices=("codex", "claude", "all"), default="all")
    install_parser.add_argument("--home", type=Path, help=argparse.SUPPRESS)

    subparsers.add_parser("list-skills", help="list centrally managed skills")
    subparsers.add_parser("validate", help="validate profiles, bundles, schema, examples, and skills")

    project_parser = subparsers.add_parser("validate-project", help="validate project config")
    project_parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())

    context_parser = subparsers.add_parser("context", help="show effective project policy")
    context_parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    context_parser.add_argument("--format", choices=("yaml", "json"), default="yaml")

    check_parser = subparsers.add_parser("check", help="check repository toolkit readiness")
    check_parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    check_parser.add_argument("--full", action="store_true", help="execute configured commands.check")
    check_parser.add_argument("--home", type=Path, help=argparse.SUPPRESS)
    check_parser.add_argument("--no-github", action="store_true", help=argparse.SUPPRESS)

    init_parser = subparsers.add_parser("init", help="initialize a consuming repository")
    init_parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    init_parser.add_argument("--type", choices=("general", "python", "django", "ios"))
    init_parser.add_argument("--profile", choices=("light", "normal", "rigorous"))
    github_group = init_parser.add_mutually_exclusive_group()
    github_group.add_argument("--github", dest="use_github", action="store_true")
    github_group.add_argument("--no-github", dest="use_github", action="store_false")
    init_parser.set_defaults(use_github=None)
    issues_group = init_parser.add_mutually_exclusive_group()
    issues_group.add_argument("--issues", dest="use_issues", action="store_true")
    issues_group.add_argument("--no-issues", dest="use_issues", action="store_false")
    init_parser.set_defaults(use_issues=None)
    init_parser.add_argument(
        "--check-command",
        metavar="COMMAND",
        help="project validation command run by 'mad-skills check --full'",
    )
    init_parser.add_argument("--yes", action="store_true", help="accept detected defaults")

    labels_parser = subparsers.add_parser("setup-github-labels", help="create missing configured labels using gh")
    labels_parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    labels_parser.add_argument("--yes", action="store_true")

    github_parser = subparsers.add_parser("setup-github", help="apply configured repository settings and labels")
    github_parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    github_parser.add_argument("--yes", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return dispatch(args)
    except MadSkillsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        return 130


def dispatch(args: argparse.Namespace) -> int:
    if args.command == "install":
        actions = install(args.target, home=args.home)
        created = sum(action.state == "create" for action in actions)
        current = sum(action.state == "current" for action in actions)
        print(f"Installed {created} link(s); {current} already current.")
        return 0
    if args.command == "list-skills":
        for path in skill_directories():
            print(path.name)
        return 0
    if args.command == "validate":
        root = find_toolkit_root()
        findings = validate_toolkit(root)
        if findings:
            for finding in findings:
                print(f"ERROR   {finding.render(root)}")
            print(f"INVALID ({len(findings)} finding(s))")
            return 1
        print("VALID")
        return 0
    if args.command == "validate-project":
        repo_root = find_repo_root(args.path)
        config_path = repo_root / ".agent/config.yaml"
        if not config_path.is_file():
            raise MadSkillsError(f"Project config is missing: {config_path}")
        errors = validate_project_data(load_yaml(config_path))
        if errors:
            for error in errors:
                print(f"ERROR   {error}")
            return 1
        print("VALID")
        return 0
    if args.command == "context":
        data = resolve_project(args.path).serializable()
        print(json.dumps(data, indent=2) if args.format == "json" else dump_yaml(data), end="\n")
        return 0
    if args.command == "check":
        result = check_project(
            args.path,
            full=args.full,
            home=args.home,
            check_github=not args.no_github,
        )
        for finding in result.findings:
            print(finding.render())
        print(result.status)
        return 1 if result.status == "NOT READY" else 0
    if args.command == "init":
        proposals = initialize_interactive(
            args.path,
            project_type=args.type,
            profile=args.profile,
            use_github=args.use_github,
            use_issues=args.use_issues,
            check_command=args.check_command,
            assume_yes=args.yes,
        )
        print("Initialized: " + ", ".join(str(item.path) for item in proposals))
        return 0
    if args.command == "setup-github-labels":
        effective = resolve_project(args.path)
        if not effective.data["github"].get("use_issues"):
            raise MadSkillsError("github.use_issues is not enabled for this project")
        labels = missing_labels(effective.repo_root, effective.data["github"])
        if not labels:
            print("GitHub labels are already ready.")
            return 0
        print("Missing labels: " + ", ".join(name for name, _ in labels))
        if not args.yes and input("Create them? [y/N]: ").strip().lower() not in {"y", "yes"}:
            raise MadSkillsError("Label setup cancelled; no labels were created")
        create_labels(effective.repo_root, labels)
        print(f"Created {len(labels)} label(s).")
        return 0
    if args.command == "setup-github":
        effective = resolve_project(args.path)
        github_config = effective.data["github"]
        if not github_workflow_enabled(github_config):
            raise MadSkillsError("GitHub workflow is not enabled for this project")
        settings = mismatched_repository_settings(effective.repo_root, github_config)
        labels = missing_labels(effective.repo_root, github_config) if github_config.get("use_issues") else []
        if not settings and not labels:
            print("GitHub repository settings and labels are already ready.")
            return 0
        if settings:
            print("Repository setting changes: " + "; ".join(settings))
        if labels:
            print("Missing labels: " + ", ".join(name for name, _ in labels))
        if not args.yes and input("Apply GitHub setup? [y/N]: ").strip().lower() not in {"y", "yes"}:
            raise MadSkillsError("GitHub setup cancelled; no repository settings or labels were changed")
        if settings:
            configure_repository(effective.repo_root, github_config)
        if labels:
            create_labels(effective.repo_root, labels)
        print(f"Applied GitHub setup: {len(settings)} setting change(s), {len(labels)} label(s).")
        return 0
    raise MadSkillsError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
