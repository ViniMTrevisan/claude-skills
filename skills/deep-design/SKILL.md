---
name: deep-design
description: Use automatically whenever a task changes how an interface looks or behaves — new or reshaped page, component, dashboard, table, form, button, modal, landing section, animation, theme, or "make it prettier / more usable / convert more". Replaces the deep-mode gate for UI-dominant work. Do not use for logic-only changes, copy-only edits, or a single isolated style value.
---

# Deep Design

Choose design depth once, then preserve: existing system, states, accessibility, motion discipline, and visual proof. Pattern libraries: `ui-polish` (buttons, badges, inputs, motion, micro-interactions) and `dashboard-ui` (KPIs, tables, filters, meters, command palette). Load the ones the task touches; `frontend-design` only when choosing a net-new visual direction.

## Precedence

UI-dominant task → this gate instead of `deep-mode`. If the same task also carries data/money/security/migration risk, run the `deep-mode` gate for that part too (sum both receipts). Visual bug ("botão desalinhado", "quebrou no mobile") starts in `deep-debug`.

## Gate

| Criterion | Score |
|---|---:|
| Net-new surface or redesign of a whole screen/section | +2 |
| At least two defensible visual/interaction directions | +2 |
| Touches 3+ components or a shared token/stylesheet | +1 |
| Reference is vague ("mais bonito", "tipo esse site") or conflicts with existing system | +1 |
| Public/conversion surface (landing, checkout, onboarding) or keyboard-heavy flow | +1 |
| Explicit quick/trivial tweak | -2 |

Score >= 2 → **heavy**. First line `[gate design: +2 motivo, +1 motivo = N → pesado]` or `[gate design: N → rápido]`. Fast mode still runs step 5 (render + look) when a renderer is available.

## Heavy pipeline

### 1. Inventory (before any code)

Read the real tokens, type scale, radii, spacing, existing component classes, and one neighbouring screen. List as `SISTEMA: <token/classe> = <valor>` the ones you will reuse. New token only when nothing existing fits — say why.

`PREMISSA: <texto> [segura|ARRISCADA]` for audience, brand constraints, reference interpretation, dark/light, devices.

### 2. Directions

2-3 directions in one line each (what the user feels + cost). Pick one; dominant criterion is usually *consistency with the existing product*, then *clarity of the primary action*. Reference sites/screens are principle sources, never pixel targets — name the principle taken from each.

### 3. State & edge sweep

Visit every row; mark irrelevant explicitly as `EDGE: <caso> → <tratamento> | n/a (<motivo>)`.

| Category | Check |
|---|---|
| Data states | empty, loading, error, 1 item, huge list, very long text/number |
| Interaction | hover, active/pressed, focus-visible, disabled, double click, touch (no hover) |
| Keyboard & a11y | tab order, Esc/Enter/arrows, labels/aria, contrast >= 4.5:1 text, hit target >= 32px |
| Responsive | 390px, ~860px breakpoint, wide; collapsed sidebars; overflow/ellipsis |
| Motion | purpose stated, <= 400ms for UI feedback, `prefers-reduced-motion` honoured, no layout jank, transform/opacity only |
| Theme & context | dark/light sections, sits correctly on every background it can appear on, print if relevant |
| Performance | no new heavy deps, no animation on scroll handlers, images sized, SSR/prerender safe |

### 4. Implement

Smallest change that delivers the direction. Reusable primitive only when used 2+ times now. Layer CSS after existing rules instead of rewriting; keep class naming and file conventions.

### 5. Visual proof (adversarial)

1. Typecheck/build/tests.
2. Render the real thing (dev server + Playwright/preview screenshot). Auth wall → temporary harness page rendering the real components with the real stylesheet; delete it before commit.
3. Look at the screenshot as a hostile reviewer: overlap, wrap, misalignment, contrast, element covered by banners/fixed UI, mobile width. Fix and re-shoot — one iteration minimum when something is off.
4. Re-read the request: every asked item delivered, nothing unrelated redesigned.

Heavy delivery ends with `[deep-design: sistema N | direções N | edges N | shots N | check ok]`; counts match visible artifacts.

## Red flags

- Writing CSS before reading the existing tokens.
- Copying a reference pixel-for-pixel or importing its fonts/colors over the brand.
- New dependency for something CSS/native does.
- Motion without reduced-motion fallback; animation that blocks input.
- Hover-only affordance on touch; focus outline removed without replacement.
- "Looks good" without a screenshot actually inspected.
- Harness/debug files left in the commit.
