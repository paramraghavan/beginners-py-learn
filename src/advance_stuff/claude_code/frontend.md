# Frontend Rules (HTML5 & Jinja2)

## Template Design

- **Inheritance**: Use a `base.html` for the skeleton (meta tags, navbar, footer) and `{% block content %}` for child
  templates.
- **Macros as Components**: One macro per logical UI component (e.g., `forms.html`, `cards.html`).
- **Semantic HTML**: Use `<header>`, `<main>`, `<footer>`, `<section>`, and `<article>` strictly.
- **Asset Management**: Use `url_for('static', filename='...')` for all CSS, JS, and images.

## State & Interactivity

- **Server-side State**: Use Flask `session` for user-specific data and `g` for request-level global variables.
- **Client-side**: Prefer Vanilla JS or **HTMX** for dynamic updates without full page reloads.
- **Form Validation**: Use HTML5 validation attributes (`required`, `type="email"`) in tandem with backend WTForms
  validation.

## Styling

- **BEM Naming**: Use Block-Element-Modifier for CSS classes to prevent naming collisions.
- **Modern CSS**: Use CSS Variables for themes and Flexbox/Grid for layouts. No `bootstrap` utility-class soup unless
  requested.