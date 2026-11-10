---
name: writing-plans
description: Use when approved work has multiple meaningful implementation steps, crosses modules or projects, or needs explicit sequencing, verification, rollback, or handoff before code changes begin. Do not use for a small self-contained edit whose path is already clear.
---

# Writing Plans

Produce a proportional, executable plan. The plan should remove ambiguity, not duplicate obvious code.

## Plan contents

Start with goal, chosen approach, scope boundaries, and relevant constraints. Then create ordered tasks containing:

- exact files or symbols to create/modify;
- intended behavior or contract;
- dependencies and ordering reasons;
- focused verification command and expected evidence;
- rollback or recovery step when failure can leave partial state;
- commit boundary only when the user or repository workflow calls for commits.

For behavior changes and bug fixes, prefer the smallest failing test or reproducible check before implementation, then the minimal change and regression verification. Include code snippets only for non-obvious contracts, signatures, migrations, or algorithms. Do not paste routine boilerplate the implementer can derive safely.

Tasks should be coherent units, usually 10-30 minutes, rather than artificial one-line steps. Split when a task crosses an authorization boundary, can fail independently, or needs its own verification.

## Required quality

- No `TBD`, `TODO`, vague "handle errors", or unnamed tests.
- Every stated requirement maps to at least one task.
- Later tasks use the same names and contracts introduced earlier.
- Preserve unrelated dirty changes and identify exact staging scope.
- Distinguish local validation, deployed state, and external-provider acceptance.
- Never assume permission to push, merge, deploy, migrate, or mutate external systems.

## Self-review and handoff

Before saving, scan for missing requirements, placeholders, inconsistent names, impossible ordering, and unverified completion claims. Fix them inline.

Save to `docs/superpowers/plans/YYYY-MM-DD-<topic>.md` unless the user or repository specifies another location. Then offer sequential execution with `executing-plans`. Do not dispatch subagents unless the user explicitly requests them.
