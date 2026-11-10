---
name: code-review
description: Use when the user asks to review a pull request, branch, commit, or diff for correctness. Read-only by default. Posting comments, applying fixes, approving, or changing PR state requires an explicit request.
---

# Code Review

Find actionable correctness problems with evidence. Do not optimize for issue count.

## Workflow

1. Resolve the exact target and status. For a PR, check whether it is open, non-draft, and reviewable.
2. Read applicable `AGENTS.md`/`CLAUDE.md` files and inspect the full changed diff without overwriting local work.
3. Trace changed behavior through direct callers, contracts, schemas, tests, and relevant history. Read broader history only when it can answer a specific uncertainty.
4. Review for correctness, regressions, security/authorization, data integrity, error handling, concurrency, dates/money, and repository-rule violations. Ignore style-only preferences unless they create a real defect.
5. Run focused tests, typechecks, or builds when feasible and proportionate. Report exactly what ran; CI existence is not proof that current changes pass.
6. Re-check each candidate finding against the actual diff. Keep high-confidence issues that are introduced or exposed by the target change.

## Output

Lead with findings ordered by severity. Each finding includes location, failure scenario, evidence, impact, and the smallest credible direction for correction. Distinguish confirmed defects from unresolved questions. If no findings remain, say so and list validation gaps.

## Boundaries

- Single-agent by default. Use subagents only when explicitly requested.
- Read-only review does not authorize comments, approvals, fixes, pushes, or state changes.
- Never comment on a PR unless explicitly requested in the current task.
- Do not report pre-existing unrelated issues as findings on the reviewed change.
- Use full SHAs for GitHub source links when links are needed.
