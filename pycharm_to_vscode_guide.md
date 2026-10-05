# PyCharm to Visual Studio Code Transition Guide

Transitioning from PyCharm to Visual Studio Code (VS Code) is straightforward once you configure the right extensions and settings. While PyCharm is an out-of-the-box IDE, VS Code is a lightweight, modular editor that becomes a powerful Python IDE when properly configured.

## 1. Key Conceptual Shift

| Concept | PyCharm | Visual Studio Code | 
| ----- | ----- | ----- | 
| **Philosophy** | Full-featured IDE out of the box | Lightweight core editor expanded via extensions | 
| **Project Config** | Stored in `.idea/` folder (XML files) | Stored in `.vscode/` folder (`settings.json`, `launch.json`) | 
| **Central Navigation** | Search Everywhere (`Double Shift`) | Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) | 
| **Interpreter Setup** | Bottom-right status bar menu | `Python: Select Interpreter` command or Environment panel | 

## 2. Step 1: Install Essential Extensions

Open the Extensions view (`Ctrl+Shift+X` on Windows/Linux or `Cmd+Shift+X` on macOS) and install these extensions:

1. **Python** (`ms-python.python`): Core language support, auto-detection of environments (`.venv`, Conda, Poetry).

2. **Pylance** (`ms-python.vscode-pylance`): High-performance language server that provides type checking, auto-imports, and code completion (similar to JetBrains indexing).

3. **Python Debugger** (`ms-python.debugpy`): Official debugging engine for Python.

4. **IntelliJ IDEA Keybindings** (`justin-gilles.intellij-idea-keybindings`): Maps standard PyCharm shortcuts into VS Code.

5. **Ruff** (`charliermarsh.ruff`) or **Black Formatter** (`ms-python.black-formatter`): Fast code formatting and linting as you type or save.

## 3. Step 2: Keyboard Shortcuts & Navigation

By installing the **IntelliJ IDEA Keybindings** extension, your favorite JetBrains shortcuts will work right away:

* `Shift + F6` $\rightarrow$ Rename symbol across project

* `Ctrl + Alt + L` / `Cmd + Option + L` $\rightarrow$ Reformat code

* `Ctrl + /` / `Cmd + /` $\rightarrow$ Toggle line comment

* `Alt + Enter` / `Option + Enter` $\rightarrow$ Quick fixes / code actions

* `Ctrl + B` / `Cmd + B` $\rightarrow$ Go to definition

> **Important Note on `Double Shift`:**
>
> VS Code's core keyboard engine does not natively support double-tap modifiers like `Double Shift`. To search for files or actions in VS Code, use:
>
> * `Ctrl + P` / `Cmd + P`: Quick Open (Search files by name)
>
> * `Ctrl + Shift + P` / `Cmd + Shift + P`: Command Palette (Search commands and settings)

## 4. Step 3: Replicating the PyCharm Look & Feel

To make VS Code closely emulate PyCharm's aesthetic and interface layout, configure these four layers:

### A. Color Theme (JetBrains / Darcula Palette)

1. Open Extensions (`Ctrl+Shift+X` or `Cmd+Shift+X`).

2. Search for and install **JetBrains Dark Theme** or **Darcula Theme**.

3. Activate it: Press `Ctrl+K` then `Ctrl+T` (macOS: `Cmd+K` then `Cmd+T`) and select **JetBrains Dark**.

### B. Typography & Ligatures (JetBrains Mono)

1. Download and install the [JetBrains Mono](https://www.jetbrains.com/lp/mono/) font on your system.

2. In VS Code Settings (`Ctrl+,` or `Cmd+,`), search for **Font Family** and set it to:

   ```text
   'JetBrains Mono', Consolas, 'Courier New', monospace
   ```

3. Search for **Font Ligatures**, click **Edit in settings.json**, and enable ligatures:

   ```json
   "editor.fontLigatures": true
   ```

### C. File Icons & Project Tree Behavior

1. Search for and install the **JetBrains Icons** (or **Material Icon Theme**) extension.

2. Activate icons via `Ctrl+K` then `Ctrl+I` (macOS: `Cmd+K` then `Cmd+I`) and choose **JetBrains Icons**.

3. Adjust folder nesting to match PyCharm's tree view by adding these lines to your `settings.json`:

   ```json
   "workbench.tree.indent": 16,
   "explorer.compactFolders": false
   ```

   *(Note: Setting `compactFolders` to `false` stops VS Code from collapsing single nested directories like `app/services/` into one line).*

### D. UI Layout & Tool Windows

* **Structure Window (PyCharm's Class/Function Tree):** In the Explorer panel (`Ctrl+Shift+E`), drag the **Outline** section header to the primary sidebar strip to make it a standalone panel, mimicking PyCharm's **Structure** tool window.

* **Bottom Panel & Terminal:** Toggle the bottom area with `Ctrl+~` / `Cmd+~`. You can drag tabs inside this panel (**Terminal**, **Debug Console**, **Problems**) to rearrange them like PyCharm's tool tabs.

* **Interpreter Status Bar:** Ensure the status bar is visible (`View` $\rightarrow$ `Appearance` $\rightarrow$ `Status Bar`). Opening any Python file displays your active interpreter in the bottom-right corner.

## 5. Step 4: Python Environment Management

PyCharm manages virtual environments automatically via GUI dialogs. In VS Code:

1. **Selecting an Interpreter:**

   * Press `Ctrl+Shift+P` / `Cmd+Shift+P`.

   * Type `Python: Select Interpreter`.

   * Pick your project's `.venv`, Conda environment, or global Python installation.

2. **Terminal Activation:**

   * Opening a new integrated terminal (`Ctrl + ~` / `Cmd + ~`) automatically activates your chosen virtual environment.

## 6. Step 5: Configuring Auto-Save & Auto-Formatting

PyCharm automatically saves changes on focus loss and formats on demand. Add the following to your VS Code `settings.json` (accessible via Command Palette $\rightarrow$ `Preferences: Open User Settings (JSON)`):

```json
{
  // Auto-save behavior matching PyCharm
  "files.autoSave": "onFocusChange",

  // Code formatting configuration
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
      "source.organizeImports": "always"
    }
  },

  // Type checking via Pylance
  "python.analysis.typeCheckingMode": "basic",

  // Typography & Layout adjustments matching PyCharm
  "editor.fontFamily": "'JetBrains Mono', Consolas, 'Courier New', monospace",
  "editor.fontLigatures": true,
  "workbench.tree.indent": 16,
  "explorer.compactFolders": false
}
```

## 7. Step 6: Running and Debugging

* **Quick Run:** Click the **Play** button in the top-right corner of an open Python file to run it in the terminal.

* **Debugging:** Click on the left margin to place breakpoints. Press `F5` to start debugging.

* **Custom Configurations:** Click the **Run and Debug** icon on the sidebar (`Ctrl+Shift+D` / `Cmd+Shift+D`) and select **create a launch.json file**. This creates a `.vscode/launch.json` file where you can pass arguments, environment variables, or specify main entry points.

### Sample `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

## Quick Reference Summary

1. Install **Python**, **Pylance**, **Python Debugger**, and **IntelliJ IDEA Keybindings**.

2. Use `Ctrl+Shift+P` / `Cmd+Shift+P` whenever you need a tool, command, or setting.

3. Select your Python interpreter once per project via `Python: Select Interpreter`.

4. Save settings in `.vscode/` to share configs across your team.