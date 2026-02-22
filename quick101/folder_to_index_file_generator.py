#!/usr/bin/env python3
"""
Scan all files in that folder (recursively) and generate:
cheatsheet/index.md (Markdown index — Markdown files open as rendered Markdown on GitHub)
cheatsheet/index.html (HTML index — HTML files render as HTML in a browser)
In index.md, HTML links include a “Preview” link that renders HTML via htmlpreview.github.io (useful because GitHub typically shows HTML as source when clicked).
"""

from __future__ import annotations

import os
import html
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# --- Config (auto-detected defaults are fine) ---
REPO_OWNER = "paramraghavan"
REPO_NAME = "beginners-py-learn"
BRANCH = "main"
ROOT_DIRNAME = "cheatsheet"  # this script should live inside /cheatsheet

# If you move this script elsewhere, update ROOT_DIR to point to the cheatsheet folder.
ROOT_DIR = Path(__file__).resolve().parent

# File patterns to ignore
IGNORE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    "index.md",
    "index.html",
    "folder_to_index_file_generator.py",
}
IGNORE_DIRS = {".git", ".github", "__pycache__", "node_modules", ".venv", "venv"}


def is_ignored(path: Path) -> bool:
    if path.name in IGNORE_NAMES:
        return True
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    return False


def collect_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and not is_ignored(p):
            files.append(p)
    return sorted(files, key=lambda x: (str(x.parent).lower(), x.name.lower()))


def rel_posix(p: Path) -> str:
    return p.relative_to(ROOT_DIR).as_posix()


def github_blob_url(rel_path: str) -> str:
    # Points to GitHub "blob" page (good for markdown rendering; HTML will usually show source)
    return f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH}/{ROOT_DIRNAME}/{rel_path}"


def html_preview_url(rel_path: str) -> str:
    # Renders HTML via htmlpreview.github.io
    # Works with the GitHub blob URL (htmlpreview fetches and serves it)
    return f"https://htmlpreview.github.io/?{github_blob_url(rel_path)}"


def pretty_title(rel_path: str) -> str:
    # Use filename without extension as a friendly label
    name = Path(rel_path).name
    stem = Path(rel_path).stem
    # Replace underscores/dashes with spaces, title-case lightly
    label = stem.replace("_", " ").replace("-", " ").strip()
    return label if label else name


def group_by_folder(files: List[Path]) -> List[Tuple[str, List[Path]]]:
    grouped = {}
    for f in files:
        folder = f.parent.relative_to(ROOT_DIR).as_posix()
        grouped.setdefault(folder, []).append(f)
    return sorted(grouped.items(), key=lambda x: x[0].lower())


def build_index_md(files: List[Path]) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(f"# Cheatsheet Index")
    lines.append("")
    lines.append(f"_Auto-generated on {now} by `generate_indexes.py`_")
    lines.append("")
    lines.append("## How links work")
    lines.append("")
    lines.append("- **Markdown (`.md`)** links open rendered on GitHub.")
    lines.append("- **HTML (`.html`)** has two links:")
    lines.append("  - **Open (repo link):** opens the file in GitHub (often shows source).")
    lines.append("  - **Preview:** renders the HTML via **htmlpreview.github.io**.")
    lines.append("")

    for folder, f_list in group_by_folder(files):
        heading = folder if folder not in ("", ".") else "(root)"
        lines.append(f"## {heading}")
        lines.append("")
        for f in f_list:
            rp = rel_posix(f)
            ext = f.suffix.lower()

            if ext == ".md":
                # Relative link so GitHub renders it as markdown
                lines.append(f"- **{pretty_title(rp)}** — [`{rp}`]({rp})")
            elif ext in (".html", ".htm"):
                # Relative open + preview
                lines.append(
                    f"- **{pretty_title(rp)}** — [`{rp}`]({rp}) "
                    f"([Preview]({html_preview_url(rp)}))"
                )
            else:
                # Other files: link relative
                lines.append(f"- `{rp}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_index_html(files: List[Path]) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Build list items grouped by folder
    body_parts = []
    for folder, f_list in group_by_folder(files):
        heading = folder if folder not in ("", ".") else "(root)"
        body_parts.append(f'<section class="card">')
        body_parts.append(f"<h2>{html.escape(heading)}</h2>")
        body_parts.append("<ul>")
        for f in f_list:
            rp = rel_posix(f)
            ext = f.suffix.lower()
            label = html.escape(pretty_title(rp))
            rp_esc = html.escape(rp)

            if ext == ".md":
                # For HTML index, open markdown via GitHub (renders nicely there)
                body_parts.append(
                    f'<li><span class="name">{label}</span> — '
                    f'<a href="{github_blob_url(rp)}" target="_blank" rel="noopener">Open on GitHub</a> '
                    f'<span class="muted">({rp_esc})</span></li>'
                )
            elif ext in (".html", ".htm"):
                # Local open relative + GitHub preview option
                body_parts.append(
                    f'<li><span class="name">{label}</span> — '
                    f'<a href="{rp_esc}" target="_blank" rel="noopener">Open (local)</a> · '
                    f'<a href="{html_preview_url(rp)}" target="_blank" rel="noopener">Preview (htmlpreview)</a> '
                    f'<span class="muted">({rp_esc})</span></li>'
                )
            else:
                body_parts.append(
                    f'<li><code>{rp_esc}</code></li>'
                )
        body_parts.append("</ul>")
        body_parts.append("</section>")

    body_html = "\n".join(body_parts)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Cheatsheet Index</title>
  <style>
    :root {{
      --bg: #0b1020;
      --card: #111a33;
      --text: #e7ecff;
      --muted: rgba(231, 236, 255, 0.70);
      --link: #9fb4ff;
      --border: rgba(231, 236, 255, 0.12);
    }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Apple Color Emoji", "Segoe UI Emoji";
      background: radial-gradient(1200px 600px at 20% 10%, rgba(159,180,255,0.25), transparent 60%),
                  radial-gradient(900px 500px at 80% 20%, rgba(80,200,180,0.18), transparent 55%),
                  var(--bg);
      color: var(--text);
      padding: 28px 18px 60px;
    }}
    .wrap {{
      max-width: 980px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 18px;
    }}
    h1 {{
      font-size: 28px;
      margin: 0 0 8px;
      letter-spacing: 0.2px;
    }}
    .sub {{
      color: var(--muted);
      margin: 0;
      font-size: 14px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      margin-top: 18px;
    }}
    .card {{
      background: rgba(17, 26, 51, 0.72);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 14px 14px 10px;
      backdrop-filter: blur(8px);
    }}
    .card h2 {{
      margin: 0 0 10px;
      font-size: 16px;
      color: rgba(231, 236, 255, 0.92);
    }}
    ul {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    li {{
      padding: 8px 0;
      border-top: 1px solid rgba(231, 236, 255, 0.08);
      line-height: 1.35;
    }}
    li:first-child {{
      border-top: none;
      padding-top: 0;
    }}
    a {{
      color: var(--link);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .name {{
      font-weight: 600;
    }}
    .muted {{
      color: var(--muted);
      font-size: 12px;
      margin-left: 6px;
    }}
    code {{
      color: rgba(231, 236, 255, 0.85);
      background: rgba(231, 236, 255, 0.06);
      padding: 2px 6px;
      border-radius: 8px;
      border: 1px solid rgba(231, 236, 255, 0.08);
    }}
    footer {{
      margin-top: 20px;
      color: var(--muted);
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Cheatsheet Index</h1>
      <p class="sub">Auto-generated on {html.escape(now)} by <code>generate_indexes.py</code></p>
      <p class="sub">Tip: HTML files render when opened in a browser. Use “Preview (htmlpreview)” for a rendered view from GitHub.</p>
    </header>

    <div class="grid">
      {body_html}
    </div>

    <footer>
      <div>Repo: <a href="https://github.com/{REPO_OWNER}/{REPO_NAME}/tree/{BRANCH}/{ROOT_DIRNAME}" target="_blank" rel="noopener">{REPO_OWNER}/{REPO_NAME}/{ROOT_DIRNAME}</a></div>
    </footer>
  </div>
</body>
</html>
"""


def main() -> None:
    if ROOT_DIR.name != ROOT_DIRNAME:
        print(f"[WARN] This script is expected to live inside '/{ROOT_DIRNAME}'.")
        print(f"       Current folder is: {ROOT_DIR}")
        print("       It will still run, but links may be off if not in the cheatsheet folder.")

    files = collect_files(ROOT_DIR)
    md = build_index_md(files)
    html_doc = build_index_html(files)

    (ROOT_DIR / "index.md").write_text(md, encoding="utf-8")
    (ROOT_DIR / "index.html").write_text(html_doc, encoding="utf-8")

    print(f"Generated:")
    print(f" - {ROOT_DIR / 'index.md'}")
    print(f" - {ROOT_DIR / 'index.html'}")
    print(f"Files indexed: {len(files)}")


if __name__ == "__main__":
    main()
