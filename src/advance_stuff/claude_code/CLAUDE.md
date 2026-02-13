# CLAUDE.md — Maximum Quality Code Generation Rules

## Core Principles
1. **Plan-first** — enter plan mode before any non-trivial task. Outline approach, identify affected files, and get approval before writing code.
2. **Verify-after** — compile, lint, test, and confirm every output before reporting done. Never say "done" without verification.
3. **Minimal diffs** — change only what's necessary. Do not refactor unrelated code, rename variables for style, or "improve" working code unless explicitly asked.
4. **Read before write** — always read the full file/module before editing. Understand existing patterns, imports, and conventions first.
5. **Single responsibility per change** — one logical change per edit. Don't bundle unrelated fixes.

## Token Optimization
- IMPORTANT: Use the full context window. Do not truncate, summarize, or abbreviate code output unless explicitly asked.
- IMPORTANT: When generating code, produce complete, runnable implementations — never use placeholder comments like `// ... rest of implementation` or `// TODO: implement this`.
- IMPORTANT: When editing, show the complete modified function/class/block — not just the changed lines with `...` ellipsis around them.
- When reading large files, use targeted reads (line ranges) rather than reading entire files when only a specific section is needed.
- Batch related file reads together before starting edits to build full context.
- When the context window is getting full, use `/compact` with instructions on what to preserve before continuing.
- Prefer precise tool calls over exploratory ones — plan which files to read before reading them.

## Code Quality Standards

### General
- Write production-grade code, not prototypes. Every output should be deployable.
- All functions/methods must have proper error handling — no bare `except`, no swallowed exceptions, no unhandled promise rejections.
- Use the language's type system fully: type hints (Python), TypeScript over JavaScript, generics where appropriate.
- Prefer explicit over implicit. Avoid magic numbers, magic strings, and implicit type coercion.
- Name variables and functions descriptively. A name should explain *what* and *why*, not just *how*.
- IMPORTANT: Never generate code with known security vulnerabilities (SQL injection, XSS, path traversal, hardcoded secrets, etc.).
- Follow the principle of least surprise — code should do what a reader expects.
- DRY (Don't Repeat Yourself) — extract shared logic into reusable functions/modules.
- Prefer composition over inheritance.
- Keep functions short and focused — one function, one job, one level of abstraction.
- Use early returns to reduce nesting.
- Constants go at the top of the file or in a dedicated constants module.

### Error Handling
- Use custom error types/classes for domain-specific errors.
- Always provide context in error messages — what failed, what was expected, what was received.
- Log errors with enough context to debug without reproducing.
- Propagate errors to callers that can handle them; don't catch and ignore.
- Use Result/Either patterns where appropriate instead of thrown exceptions.

### Testing
- Every new function/endpoint/feature must include tests.
- Test the happy path, edge cases, and error cases.
- Use descriptive test names that explain the scenario: `test_user_creation_fails_when_email_already_exists`.
- Tests must be deterministic — no flaky tests, no dependency on external services, no time-dependent assertions without mocking.
- Use fixtures and factories for test data, not hardcoded values scattered across tests.
- Assert specific values, not just truthiness.
- IMPORTANT: Run the full test suite and confirm all tests pass before reporting a task as complete.

### Documentation
- Add docstrings/JSDoc to all public functions, classes, and modules.
- Document *why*, not *what* — the code shows what, comments explain why.
- Include parameter types, return types, and exception/error conditions in docstrings.
- Keep README and API docs in sync with code changes.
- Do not add obvious comments like `// increment counter` above `counter++`.

### Git & Commits
- Write Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
- Each commit should be atomic — one logical change that compiles and passes tests.
- Never commit secrets, credentials, or environment-specific config.
- Always review the diff before committing.

## Code Generation Patterns

### When Creating New Files
1. Start with imports/dependencies at the top.
2. Define constants and types/interfaces.
3. Implement core logic.
4. Export public API.
5. Add comprehensive error handling.
6. Include inline documentation.
7. Create corresponding test file.

### When Modifying Existing Files
1. Read the entire file first to understand structure and patterns.
2. Match existing code style exactly — indentation, naming, import style, comment style.
3. Preserve existing patterns even if you'd do it differently.
4. Run lint and tests after every edit.
5. If a change requires updates in other files (imports, types, tests), make all of them.

### When Debugging
1. Read the error message and full stack trace carefully.
2. Identify the root cause, not just the symptom.
3. Check for similar patterns elsewhere in the codebase that might have the same bug.
4. Fix the root cause, add a test that would have caught it, then verify.
5. Never apply bandaid fixes without understanding why the bug exists.

### When Refactoring
1. Ensure comprehensive test coverage exists BEFORE refactoring.
2. Make refactoring changes in small, verifiable steps.
3. Run tests after each step.
4. Do not change behavior during refactoring — only structure.
5. If tests don't exist, write them first, then refactor.

## Architecture Guidelines
- Separate concerns: data access, business logic, and presentation in distinct layers.
- Use dependency injection for testability.
- Keep external dependencies behind interfaces/abstractions so they can be swapped.
- Prefer stateless functions over stateful classes where possible.
- Configuration should come from environment variables or config files, never hardcoded.
- Design APIs with backwards compatibility in mind.

## Workflow Rules
- IMPORTANT: Before starting any task, confirm you understand the requirements. Ask clarifying questions if anything is ambiguous.
- IMPORTANT: After completing a task, provide a brief summary of what was changed and why.
- When a task is too large for one context window, break it into a plan saved to `Plan.md`, complete one section per session, and update the plan after each session.
- Use `/compact` when context is getting crowded, preserving key decisions and current state.
- If you make a mistake, acknowledge it, explain what went wrong, and fix it properly — don't paper over it.

## Forbidden Patterns
- NEVER use `any` type in TypeScript (use `unknown` + type guards instead).
- NEVER use `eval()`, `exec()`, or dynamic code execution.
- NEVER hardcode credentials, API keys, tokens, or secrets.
- NEVER disable linting rules with inline comments unless absolutely necessary and explained.
- NEVER use `!important` in CSS unless overriding third-party styles.
- NEVER commit `console.log` / `print` debugging statements.
- NEVER use `var` in JavaScript — always `const` or `let`.
- NEVER ignore TypeScript/compiler errors with `@ts-ignore` or `// @ts-nocheck`.
- NEVER write empty catch blocks.
- NEVER use synchronous I/O in async contexts.
