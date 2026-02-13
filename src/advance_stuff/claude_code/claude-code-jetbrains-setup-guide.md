# Claude Code + JetBrains Community Edition Setup Guide

## Part 1: Setting Up Claude Code with JetBrains Community Edition

### Prerequisites

- **Node.js 18+** — required for the Claude Code CLI ([download](https://nodejs.org))
- **JetBrains Community Edition IDE** — IntelliJ IDEA Community, PyCharm Community, etc.
- **Claude Pro, Max, or Team plan** — or an Anthropic API key (Claude Code is not free)

### Step 1: Install the Claude Code CLI

Open your terminal and install globally via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

> **Tip:** Avoid using `sudo` — it causes permission issues and makes upgrades painful. If you get permission errors, fix your npm prefix instead:
> ```bash
> mkdir ~/.npm-global
> npm config set prefix '~/.npm-global'
> # Add to your shell profile (.bashrc, .zshrc, etc.):
> export PATH=~/.npm-global/bin:$PATH
> ```

### Step 2: Authenticate

Run `claude` once from your terminal to trigger the OAuth sign-in flow:

```bash
claude
```

This opens your browser for authentication. Sign in with your Anthropic account.

### Step 3: Install the JetBrains Plugin

1. Open your JetBrains IDE (IntelliJ IDEA Community, PyCharm Community, etc.)
2. Go to **Settings → Plugins → Marketplace**
3. Search for **"Claude Code [Beta]"** (publisher: Anthropic PBC)
4. Click **Install**
5. **Restart your IDE** completely

> **Note:** The Claude Code plugin works with Community Edition — it's a standard marketplace plugin that doesn't require Ultimate features.

### Step 4: Launch Claude Code from the IDE

Open the **integrated terminal** inside your JetBrains IDE (`Alt+F12`), navigate to your project root, and run:

```bash
claude
```

All integration features activate automatically when Claude Code detects the JetBrains IDE.

### Step 5: Verify the Integration

You should now have access to these features:

- **Quick launch:** `Ctrl+Esc` (Windows/Linux) or `Cmd+Esc` (Mac) opens Claude Code with current context
- **Diff viewing:** Code changes appear in the native JetBrains diff viewer
- **Selection context:** Your current selection/open tab is automatically shared with Claude
- **File references:** `Alt+Ctrl+K` (Linux/Windows) or `Cmd+Option+K` (Mac) inserts `@File#L1-99` references
- **Diagnostic sharing:** IDE lint/syntax errors are automatically shared with Claude

### Troubleshooting

| Problem | Fix |
|---------|-----|
| Plugin can't find `claude` command | If using nvm/mise/asdf, the IDE may not inherit your shell PATH. Set a custom command in the plugin settings (e.g., `/home/you/.npm-global/bin/claude`) |
| Plugin doesn't activate | Ensure you fully restarted the IDE after installation |
| Features not working | Make sure you're running `claude` from the IDE's **integrated terminal**, not an external one |
| WSL issues | See Anthropic's [WSL troubleshooting guide](https://code.claude.com/docs/en/troubleshooting/wsl) |

### Plugin Settings

Go to **Settings → Tools → Claude Code** to configure:

- **Claude command:** Custom path to the `claude` binary
- **Suppress notification for command not found**
- **Option+Enter for multi-line prompts** (macOS)

### Alternative: Connect an External Terminal

If you prefer running Claude in a separate terminal, use the `/ide` command to connect it to your JetBrains IDE:

```bash
claude
> /ide
```

---

## Part 2: Setting Up Rules with CLAUDE.md

### What is CLAUDE.md?

`CLAUDE.md` is a markdown configuration file that Claude Code reads at the start of every session. It provides persistent, project-specific context — coding standards, commands, architecture decisions, and workflow rules — so you don't repeat yourself in every prompt.

### Where to Place CLAUDE.md

| Location | Scope |
|----------|-------|
| `~/CLAUDE.md` | Global — applies to all projects |
| `/path/to/project/CLAUDE.md` | Project — shared with your team via source control |
| `/path/to/project/.claude/rules/*.md` | Modular rules — load conditionally based on path/globs |

Claude Code loads them in order: global → parent directories → project root. All are merged into the system prompt.

### Quick Start: Auto-Generate with /init

The fastest way to create a `CLAUDE.md` is to let Claude analyze your project:

```bash
cd /your/project
claude
> /init
```

Claude scans your codebase and generates a starter `CLAUDE.md`. Review it, delete what doesn't apply, and add your specifics.

### CLAUDE.md Template

```markdown
# Project: [Your Project Name]

## About
[One-line description of what this project is and does.]

## Tech Stack
- Language: [e.g., TypeScript, Python 3.12, Java 21]
- Framework: [e.g., Next.js 15, FastAPI, Spring Boot]
- Database: [e.g., PostgreSQL 16, SQLite]
- Package manager: [e.g., pnpm, uv, gradle]

## Commands
- **Build:** `[your build command]`
- **Test all:** `[your test command]`
- **Test single:** `[your single-test command, e.g., pytest path/to/test.py -k test_name]`
- **Lint:** `[your lint command]`
- **Format:** `[your format command]`
- **Dev server:** `[your dev server command]`

## Architecture
- `src/` — [what lives here]
- `tests/` — [testing conventions]
- `config/` — [configuration files]

## Code Style
- [e.g., Use type hints on all functions]
- [e.g., Prefer composition over inheritance]
- [e.g., Max line length: 100 characters]
- [e.g., Use descriptive variable names, no single-letter vars except loop indices]

## Conventions
- [e.g., Branch naming: feature/TICKET-123-description]
- [e.g., Commit messages follow Conventional Commits]
- [e.g., All PRs require tests for new functionality]

## Important Rules
- IMPORTANT: Never modify files in `migrations/` directly — use the migration CLI
- IMPORTANT: Always run tests before committing
- [Any other critical rules]

## Testing
- [e.g., Use pytest with fixtures defined in conftest.py]
- [e.g., Mock external services, never call real APIs in tests]
- [e.g., Minimum coverage: 80%]
```

### Best Practices

**Keep it concise.** Claude reliably follows about 100–150 custom instructions. The system prompt already uses ~50, leaving ~100 for your project. CLAUDE.md and always-on rules share this budget. Aim for ~120 lines.

**Move specialized rules to `.claude/rules/` files.** These can be path-scoped so they only load when relevant, saving your instruction budget:

```
.claude/
  rules/
    frontend.md      # Only loads when working on frontend files
    database.md      # Only loads for database-related work
    testing.md       # Only loads for test files
```

**Start simple, grow organically.** Begin with build commands and core style preferences. Add rules as you encounter friction — when Claude makes an assumption you need to correct, or when a code review reveals an undocumented convention.

**Use emphasis sparingly.** Words like "IMPORTANT" or "NEVER" increase the odds Claude follows a rule, but if everything is emphasized, nothing is. Reserve emphasis for truly critical rules.

**Don't include secrets.** CLAUDE.md gets checked into source control. Never put API keys, connection strings, or other sensitive values in it.

**Include your linter/formatter.** If you use tools like ESLint, Prettier, Biome, Black, or Ruff, document the commands. Better yet, tell Claude to run them after edits:

```markdown
## After Editing
- Always run `pnpm lint --fix` after modifying TypeScript files
- Always run `ruff format .` after modifying Python files
```

### Example: Minimal CLAUDE.md for a Java Project (IntelliJ Community)

```markdown
# Project: inventory-service

## About
Spring Boot REST API for warehouse inventory management.

## Commands
- **Build:** `./gradlew build`
- **Test all:** `./gradlew test`
- **Test single:** `./gradlew test --tests "com.example.InventoryServiceTest.testCreateItem"`
- **Run:** `./gradlew bootRun`

## Architecture
- `src/main/java/com/example/` — application code
- `src/main/resources/` — config (application.yml)
- `src/test/java/` — tests mirror main structure

## Code Style
- Java 21, use records for DTOs
- Constructor injection only (no @Autowired on fields)
- All public methods must have Javadoc
- Use Optional return types instead of null

## Important Rules
- IMPORTANT: Never modify Flyway migration files after they've been applied
- IMPORTANT: Run `./gradlew test` before committing
- All new endpoints need integration tests using @SpringBootTest
```

### Custom Slash Commands (Bonus)

Store reusable prompts as markdown files in `.claude/commands/`:

```
.claude/
  commands/
    review.md         → becomes /review
    test-coverage.md  → becomes /test-coverage
```

Example `.claude/commands/review.md`:

```markdown
Review the current changes in version control. Check for:
1. Logic errors or edge cases
2. Missing error handling
3. Style violations per our CLAUDE.md
4. Missing or inadequate tests

Provide feedback as a numbered list of actionable items.
```

Then use it in any session:

```
claude> /review
```
