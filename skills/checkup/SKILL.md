---
name: checkup
description: Use when maintaining a Claude Code or Codex setup with bloated context, unused skills/plugins/MCPs, slow hooks, duplicated instructions, repeated permission prompts, or stale CLI/configuration. Do not use for ordinary project maintenance.
---

# Checkup

Measure before changing. Back up configuration; propose destructive removal; prefer reversible archives.

## Setup map

| Area | Claude Code | Codex |
|---|---|---|
| Skills | `~/.claude/skills/` | canonical `~/.agents/skills/`, links in `~/.codex/skills/` |
| Global config | `~/.claude/settings.json` | `~/.codex/config.toml` |
| Global instructions | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| Hooks | `settings.json` | `~/.codex/hooks.json` |
| Sessions | `~/.claude/projects/**/*.jsonl` | `~/.codex/sessions/**/*.jsonl` |

## Workflow

1. **Inventory:** list active skills, plugins, MCPs, hooks, instruction sizes, broken symlinks, and CLI versions.
2. **Usage:** run `python3 <skill-dir>/scripts/audit_skill_usage.py --days 30 <skill...>`. Treat `loads` as strongest evidence and assistant-side `mentions` as an upper bound. Never count system/developer prompts or injected skill catalogs as usage.
3. **Prune:** zero or near-zero usage becomes an archive proposal. Remove or disable only with explicit approval. Preserve a dated rollback path.
4. **Deduplicate:** personal style belongs globally; team/project rules belong in the repository; long conditional procedures belong in a focused skill or script. Preserve required `AGENTS.md → CLAUDE.md` symlinks.
5. **Hooks:** time synchronous hooks. Investigate Pre/Post hooks over 500 ms; asynchronous stop hooks may be longer.
6. **Permissions:** pre-approve only repeated read-only commands. Never broadly allow publishing, deletion, mutation, or generic interpreters.
7. **Validate:** JSON/TOML syntax, plugin status, live symlinks, active references, and discovery in a new session.

Back up before editing. Report secrets found in plaintext without exposing values.

## Output

Return `area | finding | action | pending approval`, plus exact backup/archive locations and any validation that requires a fresh session.
