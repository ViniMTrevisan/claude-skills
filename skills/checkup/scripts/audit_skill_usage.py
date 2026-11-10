#!/usr/bin/env python3
"""Count assistant-side skill loads and mentions without catalog false positives."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path


def assistant_chunks(record: dict) -> list[str]:
    chunks: list[str] = []

    if record.get("type") == "assistant":  # Claude Code
        for item in record.get("message", {}).get("content", []):
            if item.get("type") == "text":
                chunks.append(str(item.get("text", "")))
            elif item.get("type") == "tool_use":
                chunks.extend((str(item.get("name", "")), json.dumps(item.get("input", {}))))

    if record.get("type") == "response_item":  # Codex
        payload = record.get("payload", {})
        if payload.get("type") == "message" and payload.get("role") == "assistant":
            for item in payload.get("content", []):
                if item.get("type") in {"output_text", "text"}:
                    chunks.append(str(item.get("text", "")))
        elif payload.get("type") == "function_call":
            chunks.extend((str(payload.get("name", "")), str(payload.get("arguments", ""))))

    return chunks


def session_text(session: Path) -> str:
    chunks: list[str] = []
    try:
        with session.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    chunks.extend(assistant_chunks(json.loads(line)))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return ""
    return "\n".join(chunks)


def patterns(skill: str) -> tuple[re.Pattern[str], re.Pattern[str]]:
    escaped = re.escape(skill)
    mention = re.compile(rf"(?<![A-Za-z0-9-]){escaped}(?![A-Za-z0-9-])")
    load = re.compile(
        rf"(?:[/\\]{escaped}[/\\]SKILL\.md|\${escaped}(?![A-Za-z0-9-])|"
        rf"[\"'](?:skill|name)[\"']\s*:\s*[\"']{escaped}[\"'])",
        re.IGNORECASE,
    )
    return load, mention


def audit(root: Path, days: int, skills: list[str]) -> dict[str, dict[str, int]]:
    cutoff = time.time() - days * 86400
    results = {skill: {"loads": 0, "mentions": 0} for skill in skills}
    if not root.exists():
        return results

    compiled = {skill: patterns(skill) for skill in skills}
    for session in root.rglob("*.jsonl"):
        try:
            if session.stat().st_mtime < cutoff:
                continue
        except OSError:
            continue
        text = session_text(session)
        for skill, (load_pattern, mention_pattern) in compiled.items():
            results[skill]["loads"] += bool(load_pattern.search(text))
            results[skill]["mentions"] += bool(mention_pattern.search(text))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="+", help="Exact skill names")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--codex-root", type=Path, default=Path.home() / ".codex/sessions")
    parser.add_argument("--claude-root", type=Path, default=Path.home() / ".claude/projects")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.days < 1:
        parser.error("--days must be positive")

    data = {
        "codex": audit(args.codex_root, args.days, args.skills),
        "claude": audit(args.claude_root, args.days, args.skills),
    }
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return

    print("skill\tcodex_loads\tclaude_loads\tcodex_mentions\tclaude_mentions")
    for skill in args.skills:
        print(
            f"{skill}\t{data['codex'][skill]['loads']}\t{data['claude'][skill]['loads']}\t"
            f"{data['codex'][skill]['mentions']}\t{data['claude'][skill]['mentions']}"
        )


if __name__ == "__main__":
    main()
