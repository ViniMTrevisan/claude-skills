#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


SECTIONS = ("Goal", "Current state", "Evidence", "Decisions", "Next action", "Risks", "Boundaries", "Files")
SECRET_RE = re.compile(r"\b(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*\S+", re.IGNORECASE)
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")
PATH_RE = re.compile(r"(?:/Users/|/private/|/var/folders/|/tmp/)\S+")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|unknown later)\b", re.IGNORECASE)
IMPERATIVE_RE = re.compile(r"^(?:run|execute|open|edit|implement|add|fix|verify|create|inspect|execute|abra|edite|implemente|adicione|corrija|verifique|crie|inspecione)\b", re.IGNORECASE)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


def redact(text: str) -> str:
    text = SECRET_RE.sub(lambda match: match.group(0).split("=", 1)[0].split(":", 1)[0] + "=[REDACTED]", text)
    text = JWT_RE.sub("[REDACTED]", text)
    return PATH_RE.sub("[LOCAL_PATH]", text)


def _sections(text: str) -> tuple[list[str], dict[str, str]]:
    matches = list(re.finditer(r"^## ([^\n]+)\s*$", text, re.MULTILINE))
    order = [match.group(1).strip() for match in matches]
    values = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        values[order[index]] = text[match.end():end].strip()
    return order, values


def validate_text(text: str, max_chars: int = 6000, integration: bool = False) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    order, values = _sections(text)
    missing = [name for name in SECTIONS if name not in values]
    if missing: errors.append("Seções ausentes: " + ", ".join(missing))
    present_expected = [name for name in SECTIONS if name in values]
    if [name for name in order if name in SECTIONS] != present_expected:
        errors.append("Seções fora da ordem obrigatória")
    for name in present_expected:
        if not values[name]: errors.append(f"Seção vazia: {name}")
    if len(text) > max_chars: errors.append(f"Contrato excede {max_chars:,} caracteres".replace(",", "."))
    if PLACEHOLDER_RE.search(text): errors.append("Contrato contém placeholder")
    if redact(text) != text: errors.append("Contrato contém provável segredo ou caminho local")

    next_action = values.get("Next action", "")
    if next_action and (not IMPERATIVE_RE.search(next_action) or not ("`" in next_action or re.search(r"\b\w+[./]\w+", next_action))):
        errors.append("Next action deve iniciar com verbo imperativo e citar comando, arquivo ou objeto")
    evidence = values.get("Evidence", "")
    if evidence and "`" not in evidence:
        warnings.append("Evidence não contém comando ou caminho verificável")
    risks = values.get("Risks", "").strip().lower()
    if risks in {"none", "nenhum", "nenhum risco", "n/a"}:
        warnings.append("Risks declara apenas ausência de risco")
    if integration:
        required_markers = {
            "Evidence": ("Source ref:", "Target ref:"),
            "Decisions": ("Integration order:",),
            "Boundaries": ("Merge authorization:",),
        }
        for section, markers in required_markers.items():
            for marker in markers:
                if marker not in values.get(section, ""):
                    errors.append(f"Handoff de integração requer {marker} em {section}")
    return ValidationResult(not errors, tuple(errors), tuple(warnings))


def render_markdown(result: ValidationResult) -> str:
    lines = [f"# Handoff Contract: {'VALID' if result.valid else 'INVALID'}"]
    if result.errors:
        lines.extend(["", "## Errors", *[f"- {item}" for item in result.errors]])
    if result.warnings:
        lines.extend(["", "## Warnings", *[f"- {item}" for item in result.warnings]])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an agent handoff contract.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--max-chars", type=int, default=6000)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--integration", action="store_true")
    args = parser.parse_args(argv)
    result = validate_text(args.path.read_text(encoding="utf-8"), args.max_chars, args.integration)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(result), end="\n" if args.format == "json" else "")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
