from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from mad_skills.errors import MadSkillsError
from mad_skills.paths import PROJECT_CONFIG, find_repo_root, find_toolkit_root

Data = dict[str, Any]


@dataclass(frozen=True)
class EffectiveConfig:
    toolkit_root: Path
    repo_root: Path
    config_path: Path
    configured: bool
    data: Data
    bundles: tuple[str, ...]
    skills: tuple[str, ...]

    def serializable(self) -> Data:
        result = copy.deepcopy(self.data)
        result["resolved"] = {
            "toolkit_root": str(self.toolkit_root),
            "repo_root": str(self.repo_root),
            "config_path": str(self.config_path),
            "configured": self.configured,
            "bundles": list(self.bundles),
            "skills": list(self.skills),
        }
        return result


def load_yaml(path: Path) -> Data:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise MadSkillsError(f"Cannot read {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise MadSkillsError(f"Invalid YAML in {path}: {exc}") from exc
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise MadSkillsError(f"Expected a YAML mapping in {path}")
    return value


def deep_merge(base: Data, overlay: Data) -> Data:
    merged = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def github_workflow_enabled(github: Data) -> bool:
    return bool(
        github.get("enabled", False)
        or github.get("use_issues", False)
        or github.get("require_pull_request_for_nontrivial_work", False)
    )


def schema_validator(toolkit_root: Path | None = None) -> Draft202012Validator:
    root = toolkit_root or find_toolkit_root()
    schema_path = root / "config/project-config.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MadSkillsError(f"Cannot load project schema {schema_path}: {exc}") from exc
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_project_data(data: Data, toolkit_root: Path | None = None) -> list[str]:
    errors = []
    validator = schema_validator(toolkit_root)
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{location}: {error.message}")
    if errors:
        return errors

    profile = data["project"]["profile"]
    github = data.get("github", {})
    if github.get("enabled") is False and (
        github.get("use_issues", False) or github.get("require_pull_request_for_nontrivial_work", False)
    ):
        errors.append("github.enabled cannot be false when issue or PR workflows are required")
    if not github.get("use_issues", False) and github.get("require_issue_for_nontrivial_work", False):
        errors.append("github: issue requirements need github.use_issues: true")
    if profile == "rigorous":
        if github.get("require_pull_request_for_nontrivial_work") is False:
            errors.append("github.require_pull_request_for_nontrivial_work cannot be false for rigorous")
        if github.get("require_well_specified_pull_request_for_nontrivial_work") is False:
            errors.append(
                "github.require_well_specified_pull_request_for_nontrivial_work cannot be false for rigorous"
            )
        if github.get("open_pull_requests_as_draft_until_reviewed") is False:
            errors.append("github.open_pull_requests_as_draft_until_reviewed cannot be false for rigorous")

    decision_log = data.get("decisions", {}).get("log")
    if decision_log:
        candidate = Path(decision_log)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append("decisions.log must be a repository-relative path without '..'")
    return errors


def resolve_project(start: Path | None = None, toolkit_root: Path | None = None) -> EffectiveConfig:
    root = toolkit_root or find_toolkit_root()
    repo_root = find_repo_root(start)
    config_path = repo_root / PROJECT_CONFIG
    defaults = load_yaml(root / "config/defaults.yaml")
    configured = config_path.is_file()
    raw = load_yaml(config_path) if configured else {}
    if configured:
        errors = validate_project_data(raw, root)
        if errors:
            joined = "\n  - ".join(errors)
            raise MadSkillsError(f"Invalid {config_path}:\n  - {joined}")

    requested_profile = raw.get("project", {}).get("profile", defaults.get("project", {}).get("profile", "light"))
    profile_path = root / "profiles" / f"{requested_profile}.yaml"
    if not profile_path.is_file():
        raise MadSkillsError(f"Unknown profile: {requested_profile}")
    profile = load_yaml(profile_path)
    effective = deep_merge(defaults, profile.get("policy", {}))
    effective = deep_merge(effective, raw)
    effective.setdefault("version", 1)

    project_type = effective["project"]["type"]
    requested_bundles = [project_type, *effective["project"].get("extra_bundles", [])]
    bundles, skills = resolve_bundles(requested_bundles, root)
    return EffectiveConfig(
        toolkit_root=root,
        repo_root=repo_root,
        config_path=config_path,
        configured=configured,
        data=effective,
        bundles=tuple(bundles),
        skills=tuple(skills),
    )


def resolve_bundles(requested: list[str], toolkit_root: Path | None = None) -> tuple[list[str], list[str]]:
    root = toolkit_root or find_toolkit_root()
    bundle_order: list[str] = []
    skill_order: list[str] = []
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in bundle_order:
            return
        if name in visiting:
            raise MadSkillsError(f"Bundle include cycle involving {name}")
        path = root / "bundles" / f"{name}.yaml"
        if not path.is_file():
            raise MadSkillsError(f"Unknown bundle: {name}")
        visiting.add(name)
        bundle = load_yaml(path)
        if bundle.get("name") != name:
            raise MadSkillsError(f"Bundle name mismatch in {path}")
        for included in bundle.get("includes", []):
            visit(included)
        visiting.remove(name)
        bundle_order.append(name)
        for skill in bundle.get("skills", []):
            if skill not in skill_order:
                skill_order.append(skill)

    for requested_name in requested:
        visit(requested_name)
    return bundle_order, skill_order


def dump_yaml(data: Data) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
