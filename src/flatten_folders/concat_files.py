#!/usr/bin/env python3
"""
Script to concatenate an entire project into a single text file.
It preserves the folder hierarchy by storing relative paths in markers.
"""

import os
import argparse
from pathlib import Path


def get_file_content(file_path):
    """
    Attempts to read file content with multiple encoding fallbacks.
    """
    try:
        # Standard modern encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            # Fallback for older Windows-style files
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"
    except Exception as e:
        return f"[Error reading file: {e}]"


def create_single_project_file(source_dir, output_file):
    """
    Traverses the directory and bundles all matching files into one output.
    """
    source_dir = Path(source_dir)
    output_path = Path(output_file)

    # Directories to ignore to prevent bloat and infinite loops
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.idea', '.vscode', 'dist', 'build'}

    # Supported file extensions for extraction
    include_extensions = {
        '.py', '.txt', '.md', '.html', '.css', '.js', '.json', '.yaml', '.yml',
        '.toml', '.cfg', '.ini', '.sh', '.bash', '.sql', '.xml', '.csv',
        '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.go', '.rs', '.java',
        '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.swift', '.kt', '.example'
    }

    # Initialize content list with a header
    content_parts = [f"{'=' * 60}\nFULL PROJECT: {source_dir.name}\n{'=' * 60}\n"]
    file_count = 0

    # os.walk is used to recursively visit every subfolder
    for root, dirs, files in os.walk(source_dir):
        # Filter 'dirs' in-place to skip unwanted folders during traversal
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in sorted(files):
            file_path = Path(root) / filename

            # Filter by extension or include files with no extension (like 'README' or 'LICENSE')
            if file_path.suffix.lower() not in include_extensions and file_path.suffix != '':
                continue

            # Calculate path relative to project root (e.g., 'src/main.py')
            relative_path = file_path.relative_to(source_dir)
            separator = "-" * 50

            # Add file markers so the extractor knows where files begin/end
            content_parts.append(f"\n{separator}\nSTART FILE: {relative_path}\n{separator}\n")
            content_parts.append(get_file_content(file_path))
            content_parts.append(f"\n{separator}\nEND FILE: {relative_path}\n{separator}\n")

            file_count += 1

    # Finalize and write the bundle
    if file_count > 0:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        print(f"Success! Created {output_path} with {file_count} files.")
    else:
        print("No matching files found to concatenate.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Concatenate entire project into one file.')
    parser.add_argument('input_folder', help='Root folder to process')
    parser.add_argument('-o', '--output', default='project_bundle.txt', help='Output filename')
    args = parser.parse_args()
    create_single_project_file(args.input_folder, args.output)