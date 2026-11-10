---
name: ponytail
description: Use before non-trivial code when the simplest working solution, YAGNI, deletion, native capabilities, or avoiding unnecessary abstractions/dependencies matters. Also use when the user asks for ponytail, lazy, minimal, or shortest-path mode. Do not simplify away safety, validation, accessibility, or explicit requirements.
license: MIT
---

# Ponytail

Choose the least code and ownership that correctly solves the verified problem.

## Ladder

Stop at the first rung that holds:

1. The requested thing does not need to exist → skip it and say why.
2. The repository already has the pattern/helper → reuse it.
3. Standard library or native platform covers it → use that.
4. An installed dependency already covers it → reuse it; do not add another.
5. A direct line or small local change works → avoid an abstraction.
6. Only then write the minimum new structure.

Understand the real flow first. For bugs, trace callers and fix the shared root cause; a tiny patch in the wrong layer is not minimal.

## Rules

- No speculative interfaces, factories, services, configuration, or extension points.
- Deletion and boring code beat clever flexibility.
- Prefer the fewest files after confirming the correct boundary.
- Mark a deliberate shortcut with `ponytail:` only when it has a known ceiling and upgrade condition; do not annotate ordinary simple code.
- Leave one focused runnable check for non-trivial branches, loops, parsers, state, money, or security. Reuse the project's test framework when present.

Never simplify away trust-boundary validation, data-loss prevention, error handling needed for correctness, security, accessibility, or anything explicitly requested.

## Modes

- `lite`: implement the request and mention a simpler alternative.
- `full` (default): enforce the ladder.
- `ultra`: challenge speculative requirements and prefer deletion.

Mode applies to the current task unless the user explicitly asks to keep or stop it. Keep explanations concise, but provide full reports or walkthroughs when requested.
