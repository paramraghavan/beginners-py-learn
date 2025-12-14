#!/usr/bin/env python3
"""
Script to extract files from concatenated text files created by concat_files.py
Reads the concatenated output and recreates the original file structure.

python ./extract_files.py ./concatenated_output -o ./restored
"""

import os
import re
import argparse
from pathlib import Path


def parse_concatenated_file(file_path):
    """
    Parse a concatenated file and extract individual files.
    
    Returns:
        List of tuples: (relative_path, content)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    files = []
    
    # Pattern to match file blocks
    # Looking for: START FILE: {path} ... END FILE: {path}
    pattern = r'-{50}\nSTART FILE: (.+?)\n-{50}\n(.*?)\n-{50}\nEND FILE: \1\n-{50}'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        relative_path = match.group(1).strip()
        file_content = match.group(2)
        files.append((relative_path, file_content))
    
    return files


def extract_files(concatenated_dir, output_dir, dry_run=False):
    """
    Extract files from concatenated text files.
    
    Args:
        concatenated_dir: Directory containing concatenated files
        output_dir: Directory to extract files to
        dry_run: If True, only show what would be extracted without writing
    """
    concatenated_dir = Path(concatenated_dir)
    output_dir = Path(output_dir)
    
    if not concatenated_dir.exists():
        print(f"Error: Concatenated directory '{concatenated_dir}' does not exist.")
        return 1
    
    # Find all .txt files in the concatenated directory
    concat_files = list(concatenated_dir.glob('*.txt'))
    
    if not concat_files:
        print(f"No .txt files found in '{concatenated_dir}'")
        return 1
    
    print(f"Found {len(concat_files)} concatenated file(s)")
    print(f"Output directory: {output_dir}")
    if dry_run:
        print("DRY RUN - No files will be written\n")
    else:
        print()
    
    total_files = 0
    
    for concat_file in sorted(concat_files):
        print(f"\nProcessing: {concat_file.name}")
        
        try:
            extracted = parse_concatenated_file(concat_file)
            
            if not extracted:
                print(f"  Warning: No files found in {concat_file.name}")
                continue
            
            print(f"  Found {len(extracted)} file(s)")
            
            for relative_path, content in extracted:
                # Create the full output path
                output_path = output_dir / relative_path
                
                if dry_run:
                    print(f"    Would extract: {relative_path}")
                else:
                    # Create parent directories if needed
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Write the file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"    Extracted: {relative_path}")
                
                total_files += 1
        
        except Exception as e:
            print(f"  Error processing {concat_file.name}: {e}")
    
    print(f"\n{'Would extract' if dry_run else 'Extracted'} {total_files} file(s) total")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Extract files from concatenated text files created by concat_files.py'
    )
    parser.add_argument(
        'concatenated_dir',
        help='Path to the directory containing concatenated .txt files (e.g., ./concatenated_output)'
    )
    parser.add_argument(
        '-o', '--output',
        default='./extracted_files',
        help='Output directory for extracted files (default: ./extracted_files)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be extracted without actually writing files'
    )
    parser.add_argument(
        '--file',
        help='Extract only from a specific concatenated file (e.g., project.txt)'
    )
    
    args = parser.parse_args()
    
    concatenated_dir = Path(args.concatenated_dir)
    
    # If a specific file is specified, process only that file
    if args.file:
        specific_file = concatenated_dir / args.file
        if not specific_file.exists():
            print(f"Error: File '{specific_file}' does not exist.")
            return 1
        
        # Temporarily create a list with just this file
        temp_dir = concatenated_dir
        print(f"Processing specific file: {args.file}")
        print(f"Output directory: {args.output}\n")
        
        extracted = parse_concatenated_file(specific_file)
        if not extracted:
            print(f"No files found in {args.file}")
            return 1
        
        print(f"Found {len(extracted)} file(s)")
        
        output_dir = Path(args.output)
        for relative_path, content in extracted:
            output_path = output_dir / relative_path
            
            if args.dry_run:
                print(f"  Would extract: {relative_path}")
            else:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Extracted: {relative_path}")
        
        print(f"\n{'Would extract' if args.dry_run else 'Extracted'} {len(extracted)} file(s)")
        return 0
    
    return extract_files(concatenated_dir, args.output, args.dry_run)


if __name__ == '__main__':
    exit(main())
