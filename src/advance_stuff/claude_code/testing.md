# Testing Rules (Pytest & Flask)

## Structure & Tooling

- **Framework**: Use `pytest` with the `pytest-flask` extension.
- **Fixtures**: Create a `conftest.py` with an `app` fixture (calling `create_app('testing')`) and a `client` fixture.
- **Database**: Use a separate test database. Use `db.session.rollback()` or a transaction-based cleanup after every
  test.

## Assertion Patterns

- **Status Codes**: Always assert the HTTP response code first.
- **Content**: Use `response.get_data(as_text=True)` to check for specific strings in the rendered HTML.
- **Redirections**: Assert `response.location` when testing login or form submissions.

## Mocking

- Mock external API calls using `unittest.mock.patch` or `requests-mock`.
- Never allow a test to send real emails or process real payments—mock the service layer.