---
name: context-slicer
description: Use when a task spans a large repository, long conversation, generated code, dirty workspace, or many candidate files and needs a small auditable context set. Do not use when a few obvious files and their direct tests fully define the task.
---

# Context Slicer

Start with high-signal evidence and expand only for a named gap.

## Choose the lightest path

- Up to roughly 8 obvious files, no generated/source ambiguity: shortlist manually with one reason per file.
- Larger, dirty, generated, or ambiguous scope: use `scripts/slice_context.py` with candidate JSON.

Always prioritize applicable instructions, edit targets, direct callers, contracts, focused tests, and required golden examples. Exclude unrelated dirty changes. Prefer source over generated output.

For scripted selection, each candidate includes `path`, `kind`, `reason`, optional score, and `required` when omission blocks the task. Generated candidates include their source. Large files use explicit ranges or symbols, never arbitrary first-N-line truncation.

If evidence is insufficient, expand with a specific gap and reason. Do not silently widen scope or treat the packet as authorization.

## Red flags

- Opening directories wholesale before searching.
- Running the script when manual selection is already obvious.
- Including files without a task-specific reason.
- Omitting instructions or focused tests merely to hit a file budget.
- Treating generated artifacts as canonical without checking their source.
