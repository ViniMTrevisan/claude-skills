---
name: handoff-contract
description: Use only when the user requests a handoff/transfer, or work must actually continue in another agent, model, session, host, or integration step with verified state. Do not use for ordinary completion summaries or casual references to future work.
---

# Handoff Contract

Transfer verified state, not confidence. The recipient must continue without rereading the conversation or guessing what was tested.

Use `assets/handoff-template.md` and preserve: Goal, Current state, Evidence, Decisions, Next action, Risks, Boundaries, Files. Separate facts, inferences, and pending work. Include observed commands/results, failing checks, prohibited actions, and unverified assumptions.

Do not include chain-of-thought, full transcripts, credentials, tokens, or unnecessary personal paths. `Next action` has one primary verb and an expected result.

Validate with:

```bash
python3 <skill-dir>/scripts/validate_handoff.py /tmp/handoff.md
```

Resolve errors; resolve or explain warnings. Default maximum is 6,000 characters. When invoked specifically for transfer, deliver the contract and stop rather than continuing implementation.

For branch/worktree integration, validate with `--integration` and include source/target refs, integration order, and merge authorization. Recording authorization never grants push, merge, deploy, or deletion authority.
