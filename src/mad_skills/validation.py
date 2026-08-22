from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from mad_skills.configuration import load_yaml, resolve_bundles, validate_project_data
from mad_skills.errors import MadSkillsError
from mad_skills.paths import find_toolkit_root

FRONTMATTER = re.compile(r"\A---\s*\n(?P<header>.*?)\n---\s*\n", re.DOTALL)
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class ValidationFinding:
    path: Path
    message: str

    def render(self, root: Path) -> str:
        try:
            relative = self.path.relative_to(root)
        except ValueError:
            relative = self.path
        return f"{relative}: {self.message}"


def parse_skill(path: Path) -> tuple[str, str]:
    skill_file = path / "SKILL.md"
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise MadSkillsError(f"Cannot read {skill_file}: {exc}") from exc
    match = FRONTMATTER.match(text)
    if not match:
        raise MadSkillsError("SKILL.md must start with YAML frontmatter")
    try:
        header = yaml.safe_load(match.group("header"))
    except yaml.YAMLError as exc:
        raise MadSkillsError(f"invalid frontmatter: {exc}") from exc
    if not isinstance(header, dict):
        raise MadSkillsError("frontmatter must be a mapping")
    if set(header) != {"name", "description"}:
        raise MadSkillsError("frontmatter must contain only name and description")
    name = header.get("name")
    description = header.get("description")
    if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
        raise MadSkillsError("name must use lowercase hyphen-case")
    if path.name != name:
        raise MadSkillsError(f"directory name must match skill name {name!r}")
    if not isinstance(description, str) or len(description.strip()) < 20:
        raise MadSkillsError("description must be a useful string of at least 20 characters")
    if "TODO" in text:
        raise MadSkillsError("unresolved TODO placeholder")
    return name, description


def validate_skill(path: Path, *, require_metadata: bool = True) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    try:
        name, _ = parse_skill(path)
    except MadSkillsError as exc:
        return [ValidationFinding(path, str(exc))]
    metadata_path = path / "agents/openai.yaml"
    if not metadata_path.is_file() and require_metadata:
        findings.append(ValidationFinding(metadata_path, "missing Codex UI metadata"))
    elif metadata_path.is_file():
        try:
            metadata = load_yaml(metadata_path)
            interface = metadata["interface"]
            short = interface["short_description"]
            prompt = interface["default_prompt"]
            if not 25 <= len(short) <= 64:
                findings.append(ValidationFinding(metadata_path, "short_description must be 25-64 characters"))
            if f"${name}" not in prompt:
                findings.append(ValidationFinding(metadata_path, f"default_prompt must mention ${name}"))
        except (KeyError, TypeError, MadSkillsError) as exc:
            findings.append(ValidationFinding(metadata_path, f"invalid metadata: {exc}"))
    return findings


def validate_toolkit(toolkit_root: Path | None = None) -> list[ValidationFinding]:
    root = toolkit_root or find_toolkit_root()
    findings: list[ValidationFinding] = []

    schema_path = root / "config/project-config.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        findings.append(ValidationFinding(schema_path, f"invalid JSON Schema: {exc}"))

    seen_names: dict[str, Path] = {}
    skill_root = root / "skills"
    for skill_path in sorted(path for path in skill_root.iterdir() if path.is_dir()):
        skill_findings = validate_skill(skill_path)
        findings.extend(skill_findings)
        if not skill_findings:
            name, _ = parse_skill(skill_path)
            if name in seen_names:
                findings.append(ValidationFinding(skill_path, f"duplicate skill name {name}"))
            seen_names[name] = skill_path

    defaults = load_yaml(root / "config/defaults.yaml")
    for profile_path in sorted((root / "profiles").glob("*.yaml")):
        try:
            profile = load_yaml(profile_path)
            if profile.get("name") != profile_path.stem:
                findings.append(ValidationFinding(profile_path, "profile name does not match filename"))
            if not isinstance(profile.get("policy"), dict):
                findings.append(ValidationFinding(profile_path, "profile policy must be a mapping"))
            else:
                for key_path in _unknown_policy_keys(profile["policy"], defaults):
                    findings.append(ValidationFinding(profile_path, f"unknown profile policy key {key_path}"))
        except MadSkillsError as exc:
            findings.append(ValidationFinding(profile_path, str(exc)))

    for bundle_path in sorted((root / "bundles").glob("*.yaml")):
        try:
            bundle = load_yaml(bundle_path)
            if bundle.get("name") != bundle_path.stem:
                findings.append(ValidationFinding(bundle_path, "bundle name does not match filename"))
            if set(bundle) != {"name", "includes", "skills"}:
                findings.append(ValidationFinding(bundle_path, "bundle must contain name, includes, and skills"))
            if not isinstance(bundle.get("includes"), list) or not all(
                isinstance(item, str) for item in bundle.get("includes", [])
            ):
                findings.append(ValidationFinding(bundle_path, "includes must be a string list"))
            if not isinstance(bundle.get("skills"), list) or not all(
                isinstance(item, str) for item in bundle.get("skills", [])
            ):
                findings.append(ValidationFinding(bundle_path, "skills must be a string list"))
            _, skills = resolve_bundles([bundle_path.stem], root)
            for skill in skills:
                if skill not in seen_names:
                    findings.append(ValidationFinding(bundle_path, f"references missing skill {skill}"))
        except MadSkillsError as exc:
            findings.append(ValidationFinding(bundle_path, str(exc)))

    for example in sorted((root / "examples").glob("*.yaml")):
        try:
            errors = validate_project_data(load_yaml(example), root)
            findings.extend(ValidationFinding(example, error) for error in errors)
        except MadSkillsError as exc:
            findings.append(ValidationFinding(example, str(exc)))
    return findings


def _unknown_policy_keys(policy: dict, defaults: dict, prefix: tuple[str, ...] = ()) -> list[str]:
    unknown: list[str] = []
    open_mappings = {("risk",), ("github", "labels"), ("extensions",)}
    for key, value in policy.items():
        path = (*prefix, key)
        if key not in defaults:
            if prefix not in open_mappings:
                unknown.append(".".join(path))
            continue
        if isinstance(value, dict):
            if not isinstance(defaults[key], dict):
                unknown.append(".".join(path))
            elif path not in open_mappings:
                unknown.extend(_unknown_policy_keys(value, defaults[key], path))
    return unknown
