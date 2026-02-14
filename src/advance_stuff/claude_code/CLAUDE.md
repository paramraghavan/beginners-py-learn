# CLAUDE.md — Flask & Python Quality Rules

## Core Principles

1. **Plan-first** — Outline Blueprints, database models, and route logic before coding.
2. **Application Factory** — Always use `create_app()` pattern to avoid circular imports and enable better testing.
3. **Type Safety** — Use Python type hints (`typing`) for all function signatures and variable declarations.
4. **Environment-led** — Use `.env` files for configuration; never hardcode secrets or URLs.

## Code Quality Standards

- **Structure**: Follow a modular structure using **Flask Blueprints**. Keep `routes.py`, `models.py`, and `services.py`
  separate.
- **Security**:
    - Always use `Flask-WTF` for form handling and CSRF protection.
    - Use `werkzeug.security` for password hashing.
    - Use `SQLAlchemy` ORM to prevent SQL injection.
- **Dependency Management**: Maintain a clean `requirements.txt` or `pyproject.toml`. Use virtual environments (`venv`).
- **Logic Placement**: Keep routes thin. Move complex business logic into a `services/` layer and data logic into
  `models/`.

## Error Handling

- Use `@app.errorhandler` or `@blueprint.app_errorhandler` for global exception handling.
- Return consistent JSON responses for API errors: `{"error": "Description", "code": 404}`.
- Use `flask.abort()` for intentional HTTP exceptions.