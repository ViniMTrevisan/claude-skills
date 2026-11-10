---
name: deep-mode
description: Use when beginning implementation, refactoring, design, or a technical decision where risk, ambiguity, alternatives, state, integrations, or cross-module scope may require deeper reasoning. For bug diagnosis or failing tests, use deep-debug first. Do not use for factual questions, typos, renames, formatting, or isolated config values.
---

# Deep Mode

Choose reasoning depth once. Preserve assumptions, alternatives, edge cases, implementation, and adversarial verification without loading separate skills.

## Precedence

Bug, failing test, or unexpected behavior starts with `deep-debug`, which owns reproduction and root-cause evidence. After the cause is confirmed, use this gate only when choosing or implementing the fix is itself risky or has multiple defensible approaches. Reuse diagnostic evidence; do not repeat the investigation.

UI-dominant work (page, component, dashboard, table, form, motion, "deixar mais bonito") uses `deep-design` instead of this gate; run both only when the UI task also carries data/money/security/migration risk.

## Gate

| Criterion | Score |
|---|---:|
| Irreversible or expensive to correct: production, data, migration, public API, schema | +2 |
| At least two defensible approaches | +2 |
| Touches 3+ files or crosses modules/projects | +1 |
| Requirement is ambiguous, conflicting, or underspecified | +1 |
| Shared state, concurrency, security, or money | +1 |
| Explicit quick/direct/trivial request | -2 |

Score >= 2 means **heavy**. Score < 2 means **fast**. First response line is always `[gate: N → rápido]` or, for heavy mode, `[gate: +2 motivo, +1 motivo = N → pesado]` with real components. Fast mode proceeds directly without fabricated ceremony.

## Heavy pipeline

### 1. Assumptions

List every assumption that affects the work as `PREMISSA: <texto> [segura|ARRISCADA]`. Risky means a wrong assumption can cause more than 30 minutes of rework or external harm. Ask one objective question only when it is risky and blocking; otherwise declare the safe reversible default.

### 2. Alternatives

Generate 2-3 defensible approaches before evaluating them. Compare pros, cons, and cost to change later. Choose one and name the dominant criterion. Ties go to the simplest reversible option.

### 3. Edge cases

Visit every category and mark irrelevant ones explicitly:

`EDGE: <caso> → <tratamento> | aceito sem tratamento (<motivo>)`

| Category | Check |
|---|---|
| Empty/null | null, undefined, empty string/list |
| Boundaries | 0, 1, maximum, negative, pagination edge |
| Partial state | mid-operation failure, rollback, idempotent retry |
| Concurrency | simultaneous requests, double click, race |
| Dependency failure | outage, timeout, malformed response |
| Time | timezone, DST, day/month boundary, client clock |
| Permission | wrong actor, expired token, wrong tenant/franchise |

Never simplify away validation, data-loss prevention, security, accessibility, or explicit requirements.

### 4. Implement

Implement the chosen minimum complete approach. Preserve repository conventions, unrelated work, authorization boundaries, and proportionate verification.

### 5. Adversarial check

1. Re-read the original request: every requested item delivered, nothing unrelated added.
2. Run tests/build/call; if impossible, simulate the main path with a concrete input.
3. Name the first specific production failure candidate and fix correctable issues now.
4. Review changed code/config for dead imports, debug output, broken references, invalid syntax, secrets, and violated conventions.
5. Re-run relevant verification after corrections.

Heavy delivery includes a visible check verdict and ends with `[deep: premissas N (M arriscadas) | abordagens N | edges N | check ok]`. Counts must match visible artifacts.

## Red flags

- Inflating or skipping the gate.
- Choosing before generating alternatives.
- Omitting an edge category silently.
- Saying `should work` without execution or simulation.
- Heavy mode without assumptions, alternatives, edges, check verdict, or receipt.
- Declaring "CI-ready" after running only a subset of CI steps; read the workflow and run every step of the affected jobs locally.
