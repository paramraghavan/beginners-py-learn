#!/usr/bin/env python3
"""
Script to rebuild a project's original directory structure from a
single concatenated bundle file.
"""

import os
import re
import argparse
from pathlib import Path


def extract_from_bundle(bundle_file, output_dir, dry_run=False):
    """
    Parses the bundle and recreates directories and files.
    """
    bundle_path = Path(bundle_file)
    output_base = Path(output_dir)

    if not bundle_path.exists():
        print(f"Error: Bundle file '{bundle_file}' not found.")
        return

    # Read the entire bundle into memory for regex processing
    with open(bundle_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex Logic Breakdown:
    # 1. Look for 50 dashes
    # 2. Capture the relative path after 'START FILE: '
    # 3. Use (.*?) to lazily capture all content until the 'END FILE' tag
    # 4. Use \1 backreference to ensure the END filename matches the START filename
    # 5. re.DOTALL allows the '.' to match newline characters
    pattern = r'-{50}\nSTART FILE: (.+?)\n-{50}\n(.*?)\n-{50}\nEND FILE: \1\n-{50}'
    matches = re.finditer(pattern, content, re.DOTALL)

    extracted_count = 0
    for match in matches:
        rel_path_str = match.group(1).strip()  # The captured relative path
        file_content = match.group(2)  # The captured file content

        # Combine the extraction root with the relative path from the bundle
        target_path = output_base / rel_path_str

        if dry_run:
            print(f"Would extract: {rel_path_str}")
        else:
            # Recreate the folder structure if it doesn't exist (parents=True)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"Extracted: {rel_path_str}")

        extracted_count += 1

    print(f"\nFinished. {'Total files found' if dry_run else 'Total files extracted'}: {extracted_count}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rebuild project from a single concatenated file.')
    parser.add_argument('bundle_file', help='The concatenated .txt file')
    parser.add_argument('-o', '--output', default='./restored_project', help='Where to extract files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would happen without writing')
    args = parser.parse_args()
    extract_from_bundle(args.bundle_file, args.output, args.dry_run)