---
name: deep-debug
description: Use when diagnosing a bug, failing test, regression, intermittent failure, or unexpected behavior before proposing a fix. Do not use when expected behavior is already known and only a straightforward implementation remains.
---

# Deep Debug

No production fix before the cause is supported by evidence. Change one variable at a time.

## Gate

| Criterion | Score |
|---|---:|
| Cause is not visible directly in the error/stack | +2 |
| Intermittent, production, external integration, or data-related | +2 |
| Obvious syntax, typo, or missing import in the error | -2 |

Score >= 2 uses the full process; lower scores fix directly. Print `[gate: N → rápido|pesado]` with real components when heavy. Do not also run the `deep-mode` gate during diagnosis.

## Full process

1. Define expected versus observed behavior and the smallest concrete reproduction.
2. Reproduce locally when safe. If reproduction is unavailable, collect deployed logs, traces, configuration, timestamps, or provider responses; label unconfirmed explanations as hypotheses.
3. State one hypothesis: `X causes Y because Z`.
4. Test only that hypothesis with the smallest discriminating observation before editing production code.
5. If refuted, record the evidence and test the next hypothesis. If confirmed, fix the shared root cause, not one caller's symptom.
6. Re-run the original reproduction and focused regressions. Distinguish local verification from deployment or provider acceptance.

After root cause is confirmed, invoke `deep-mode` only if the fix introduces a material design choice, risky state change, or multiple valid approaches. Reuse the collected evidence.

## Boundaries

- Never change production data/configuration, issue fiscal documents, trigger payments, or call mutating provider operations merely to reproduce a bug without explicit authorization.
- Do not combine the fix with unrelated refactoring.
- Do not change multiple causal variables in one experiment.
- Do not call a probable cause confirmed without discriminating evidence.
- Do not declare resolution without re-running the reproduction or explaining why only deployed verification remains.
