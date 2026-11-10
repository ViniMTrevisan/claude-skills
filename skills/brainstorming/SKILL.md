---
name: brainstorming
description: Use when feature behavior, product scope, UX, or architecture has multiple defensible interpretations and choosing incorrectly would cause meaningful rework. Do not use for straightforward implementation, known bug behavior, small refactors, typos, formatting, or isolated configuration changes.
---

# Brainstorming

Turn an unresolved product or technical decision into an approved design without turning every change into a ceremony.

## Gate

Use this skill only when implementation depends on a material choice. If requirements and the established repository pattern already determine the solution, proceed directly. A `deep-mode` fast gate also skips brainstorming.

## Workflow

1. Inspect applicable instructions, current behavior, nearby patterns, and relevant recent decisions.
2. State assumptions. Ask one question only when its answer materially changes scope, behavior, or architecture; otherwise use a safe reversible default.
3. Present 2-3 defensible approaches with trade-offs. Recommend one using the dominant criterion: simplicity, reversibility, safety, performance, or delivery time.
4. Present the smallest design that resolves the decision. Cover behavior, affected boundaries, data flow, failures, and verification only where relevant.
5. Obtain approval before implementing a material behavior or architecture choice.

Keep the conversation proportional. A small decision may need one short comparison and one approval. A cross-project or expensive decision may need several sections.

## Documentation and transition

Write a design document only when the work is multi-step, crosses modules/projects, is expensive to reverse, or the user/repository requires one. Use `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` unless local instructions say otherwise. Commit it only when committing is authorized and appropriate for the repository.

Before transition, check the design for missing requirements, contradictions, placeholders, and ambiguous terms. After approval:

- multi-step work → use `writing-plans`;
- small self-contained work → implement directly under the normal verification workflow.

## Visual questions

Offer a visual companion only when the next decision is genuinely easier to understand through a mockup, diagram, or side-by-side visual. Do not offer it for textual requirements or ordinary trade-offs.

## Red flags

- Designing after implementation has started.
- Asking questions whose answers do not change the design.
- Requiring a spec or commit for a trivial change.
- Presenting one real option plus straw men.
- Expanding scope beyond the user's goal.
