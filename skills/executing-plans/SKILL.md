---
name: executing-plans
description: Use when an approved written implementation plan is ready to execute sequentially with checkpoints. Do not use merely because a task has several informal thoughts or when no plan exists.
---

# Executing Plans

Execute the approved plan sequentially, preserving scope and producing evidence for each completed task.

## Workflow

1. Read the plan and applicable repository instructions. Check branch/worktree state and unrelated changes.
2. Review the plan for a blocking gap or stale assumption. Correct cheap, in-scope details; ask only when a material choice or new authorization is required.
3. For each task: mark it active, perform its steps, run its specified verification, record the observed result, then mark it complete.
4. On failure, diagnose and attempt safe in-scope corrections. Do not stop at the first ordinary test failure. Stop when the same blocker persists after three evidence-backed attempts, the plan's approach is invalid, or progress requires user authority/external state.
5. After all tasks, run the complete relevant verification, review the final diff, and compare the result with the original request and plan.

## Boundaries

- Preserve unrelated dirty work and stage only named files.
- Do not dispatch subagents unless explicitly requested.
- Do not push, merge, deploy, migrate, delete, or remove a worktree without authorization.
- Never start implementation on `main`/`master` unless explicitly permitted.
- Report local checks, remote/deployed state, and provider acceptance separately.
- When the user asks to wait for all workflows, wait for every relevant terminal result.

If complete, report evidence and remaining external steps. If blocked, report the exact blocker, attempts, evidence, preserved state, and one required user action.
