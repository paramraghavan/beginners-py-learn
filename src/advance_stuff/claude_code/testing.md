# Testing Rules

## Test Structure
- Follow Arrange → Act → Assert (AAA) pattern in every test.
- One logical assertion per test. Multiple assertions are OK only if testing the same behavior.
- Use descriptive names: `should_return_404_when_user_not_found` not `test1`.
- Group related tests with `describe`/`context` blocks.
- Keep test files next to source files or mirror the source directory structure.

## Test Data
- Use factories or builders for test data — not raw object literals scattered everywhere.
- Each test must set up its own data. Never depend on state from another test.
- Use realistic but deterministic data. Avoid `Math.random()` or timestamps without mocking.
- Clean up after tests that create side effects (database records, files, etc.).

## Mocking
- Mock at the boundary (HTTP clients, database, file system) — not internal functions.
- Verify mock calls (was the right method called with the right arguments?).
- Reset mocks between tests to prevent leakage.
- Prefer dependency injection over monkey-patching for testability.
- Use in-memory databases or test containers for integration tests.

## Coverage
- New code must have tests. No exceptions.
- Aim for meaningful coverage, not 100% line coverage — test behaviors, not implementation.
- Every bug fix must include a regression test that would have caught the bug.
- Critical paths (auth, payments, data mutations) must have integration tests.

## Performance
- Unit tests must complete in < 100ms each.
- Integration tests must complete in < 5s each.
- Use parallel test execution where possible.
- Never make real network calls in tests — mock all external services.
