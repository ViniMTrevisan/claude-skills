---
name: ui-polish
description: Use automatically when building or refining buttons, badges, chips, inputs, cards, kickers, hero sections, modals, toasts, or any micro-interaction/animation, or when asked to make an interface feel more premium, modern, alive, or to convert better. Pattern library loaded by deep-design. Do not use for backend or copy-only work.
---

# UI Polish

Principles distilled from beautifului.dev, beui.dev, rareui.com, transitions.dev, ui.shadcn.com, opensourceui.in, ui.kitze.io. Apply through the project's own tokens — never import their palettes or fonts.

## Buttons

- Hierarchy: one primary per view region; secondary = bordered surface; ghost for tertiary; danger only on destructive.
- Press feedback: `:active { transform: scale(.97-.98) }`, 120ms, custom ease (`cubic-bezier(.2,.7,.2,1)`).
- Primary depth: subtle top-light gradient + `inset 0 1px 0 rgba(255,255,255,.2)` + coloured soft shadow; hover grows shadow, not size.
- Optional shine: `::after` diagonal gradient translateX(-110% → 110%) on hover, 600-700ms, `pointer-events:none`, parent `overflow:hidden`. Primary/CTA only.
- Always `:focus-visible` ring (2px brand, offset 2px). Disabled = opacity .45 + `not-allowed`, no hover effects.

## Badges, chips, tags

- Tinted fill + tinted border: `box-shadow: inset 0 0 0 1px color-mix(in srgb, currentColor 26%, transparent)`. Radius 6px for data, pill for filters/toggles.
- Status colour carries meaning consistently across the app (red late, amber attention, green done, blue active).
- Chip selected state must differ by more than colour (fill inversion or check).

## Inputs & filters

- Segmented filter: muted label + value inside one outline ("Projeto | Todos ▾"); focus-within colours the whole outline.
- Search shows a `kbd` hint when a shortcut exists. Placeholder says what is searchable.

## Section & typography details

- Kicker above titles: mono, uppercase, letter-spaced, small pill with dot — orientation, not decoration.
- Gradient/shimmer text at most once per page (the hero accent).
- Numbers: `font-variant-numeric: tabular-nums`; muted units.

## Motion rules (transitions.dev discipline)

- Every animation answers "what changed?". Entrances: opacity + 8-18px translate + optional blur(6px→0), 300-600ms, staggered 40-80ms, once.
- Feedback ≤ 200ms; layout/overlay 160-350ms; decorative loops slow (≥ 3s) and rare.
- Animate transform/opacity/filter only. Never animate on scroll handlers; use IntersectionObserver/whileInView.
- Overlays: backdrop blur 3-8px, pop-in scale .985→1. Exit faster than enter.
- Delight (confetti, tilt, glare, auto-advance) only at a success moment or on a hero object; pointer-only; skipped under reduced motion; never breaks keyboard flow.
- `@media (prefers-reduced-motion: reduce)`: remove transforms/loops, keep opacity changes.

## Conversion details (landing)

- Primary CTA visible in hero, sticky nav, mobile bottom bar and after each proof block.
- Whole card/row clickable via `a::after { position:absolute; inset:0 }` (don't put transforms on the anchor — it traps the pseudo element).
- Social proof as compact grayscale logo strip → colour on hover.
- Official brand icons (WhatsApp, etc.) from Simple Icons paths, never hand-drawn approximations.
