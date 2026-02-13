# Frontend Rules

## Component Design
- One component per file. File name matches component name.
- Props must be typed with an interface/type, not inline.
- Destructure props in the function signature.
- Use semantic HTML elements (`<nav>`, `<main>`, `<article>`, `<section>`) — not `<div>` soup.
- Keep components under 150 lines. Extract subcomponents when exceeding this.
- Co-locate styles, tests, and types with the component.

## State Management
- Use local state first. Only lift to global state when multiple unrelated components need it.
- Derive state instead of syncing it. If a value can be computed from other state, compute it.
- Never store derived data in state.
- Use `useMemo`/`useCallback` only when you've measured a performance problem — not preemptively.

## Styling
- Use consistent units (rem for spacing/typography, px for borders/shadows).
- Design mobile-first — base styles for mobile, media queries for larger screens.
- Never use inline styles except for dynamic values that can't be expressed in CSS.
- All colors must come from the design token/theme system — no hardcoded hex values.

## Accessibility
- IMPORTANT: All interactive elements must be keyboard accessible.
- All images must have meaningful `alt` text (or `alt=""` for decorative images).
- Form inputs must have associated `<label>` elements.
- Use ARIA attributes only when semantic HTML is insufficient.
- Maintain a logical heading hierarchy (h1 → h2 → h3, no skipping).
- Color must not be the only way to convey information.
