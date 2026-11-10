---
name: frontend-design
description: Use when creating a new frontend page/component or materially reshaping an existing interface and visual design quality is part of the request. Do not use for logic-only changes, small style fixes, or implementations that must simply reproduce an already-specified design.
license: Complete terms in LICENSE.txt
---

# Frontend Design

Create polished, context-specific interfaces without overriding an established product language.

## Order of decisions

1. Inspect existing tokens, typography, components, spacing, responsive patterns, accessibility conventions, and nearby screens.
2. If a design system or supplied reference exists, preserve it. Reuse components and variables before introducing new styles or dependencies.
3. For genuinely net-new visual direction, choose one coherent concept based on purpose, audience, content, and brand—not novelty alone.
4. Implement functional states: default, loading, empty, error, disabled, focus, hover, and responsive behavior where applicable.
5. Verify visually in the real app or rendered output when possible; also run relevant code checks.

## Quality bar

- Typography, hierarchy, spacing, color, and motion form one system.
- Accessibility basics are non-negotiable: semantics, keyboard/focus behavior, contrast, labels, and reduced motion.
- Motion must explain state or reinforce hierarchy; prefer CSS/native capabilities and installed dependencies.
- Avoid generic generated aesthetics, decorative complexity without purpose, arbitrary new fonts, and fashionable patterns that conflict with the product.
- Match implementation complexity to the chosen direction. Restraint is preferable when the existing system is restrained.

Do not redesign unrelated surfaces. If the request conflicts with the existing design system, identify the conflict before expanding scope.
