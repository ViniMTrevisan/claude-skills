---
name: dashboard-ui
description: Use automatically when building or refining admin panels, internal tools, CRMs, dashboards, KPI cards, data tables, kanban boards, filters, sidebars, or command palettes. Pattern library loaded by deep-design. Do not use for marketing pages or backend-only work.
---

# Dashboard UI

Base reference: Sales CRM by kargulstudio (dark, Geist, dense, calm). Goal: scan fast, act fast, zero noise.

## Layout & navigation

- Sidebar grouped by job (e.g. Vendas / Entrega / Financeiro / Sistema) with uppercase muted 10-11px section labels; labels collapse to hairlines when the sidebar collapses.
- Counts as small badges beside nav items only when actionable.
- Page head: title + status pill left, primary action right. Secondary actions ghost/bordered.
- ⌘K / Ctrl+K command palette: native `<dialog>` + `showModal`, blurred backdrop, one input, grouped results (pages first, then entities), ↑↓/Enter/Esc, footer key hints, accent-insensitive multi-word match, load data on open, cap results (~40).

## KPI cards

- One hero KPI per screen (accent top line + brand tint); alerts tinted red only when action is needed; zero values dimmed, not shouted.
- Trend as a tiny bar sparkline (last bar = current period highlighted); progress toward goal as thin bar under the value.
- Long values must not wrap: keep decorations out of the value row.

## Tables

- Dense rows (10-12px vertical padding), uppercase 10.5px headers, tabular numbers right-aligned, first column linked/emphasised, row hover tint + inset accent edge, whole row clickable without hijacking inner links.
- Aggregates footer bar: "N em vista · soma · média" reflecting active filters.
- Empty state centred with guidance, not a lone "—".

## Meters & status

- Probability/progress as segmented tick meter (8-14 ticks); scale tone red < 34% < amber < 67% < green, or single brand/green tone for neutral progress; always `role="meter"` + aria values + visible number when precision matters.
- Status badges tinted with tinted border; same status → same colour everywhere.

## Filters

- Segmented filter pills ("Responsável | Qualquer ▾"), toggle chips for quick personal scopes ("Minhas"), search box first; push actions to the right with a spacer.
- On mobile, filters flex to full width; selects shrink with ellipsis.

## Forms & modals

- Sectioned modal: uppercase section labels with dividers, two-column grid on desktop, footer Cancel (ghost) + primary right.
- Drawer for record detail, modal for create/edit.

## Don'ts

- Charts library for a 6-bar sparkline. Rainbow palettes. Shadows on every card. Animating numbers on every render. Hiding critical actions behind hover only.
