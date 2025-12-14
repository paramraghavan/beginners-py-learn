#!/usr/bin/env python3
"""
Script to concatenate all files in each folder into a single text file.
Each file's content is wrapped with start/end separators showing the filename.
"""

import os
import argparse
from pathlib import Path


def get_file_content(file_path):
    """Read file content, handling different encodings."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"
    except Exception as e:
        return f"[Error reading file: {e}]"


def concatenate_folder_files(folder_path, output_dir, recursive_content=False):
    """
    Concatenate all files in a folder into a single text file.
    
    Args:
        folder_path: Path to the folder to process
        output_dir: Directory to save output files
        recursive_content: If True, include files from subfolders in parent's output
    """
    folder_path = Path(folder_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Skip hidden folders and common non-code directories
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.idea', '.vscode'}
    
    # File extensions to include (add more as needed)
    include_extensions = {
        '.py', '.txt', '.md', '.html', '.css', '.js', '.json', '.yaml', '.yml',
        '.toml', '.cfg', '.ini', '.sh', '.bash', '.sql', '.xml', '.csv',
        '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.go', '.rs', '.java',
        '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.swift', '.kt','.example'
    }
    
    processed_folders = set()
    
    def process_folder(current_folder):
        """Process a single folder and create its concatenated file."""
        current_folder = Path(current_folder)
        
        if current_folder.name in skip_dirs:
            return
        
        if current_folder in processed_folders:
            return
        
        # Get all files directly in this folder
        files = []
        for item in sorted(current_folder.iterdir()):
            if item.is_file():
                # Include files with matching extensions or no extension
                if item.suffix.lower() in include_extensions or item.suffix == '':
                    files.append(item)
        
        # Only create output if there are files
        if files:
            output_filename = f"{current_folder.name}.txt"
            output_path = output_dir / output_filename
            
            content_parts = []
            content_parts.append(f"{'='*60}")
            content_parts.append(f"FOLDER: {current_folder}")
            content_parts.append(f"{'='*60}\n")
            
            for file_path in files:
                relative_path = file_path.name
                separator = "-" * 50
                
                content_parts.append(f"\n{separator}")
                content_parts.append(f"START FILE: {relative_path}")
                content_parts.append(f"{separator}\n")
                
                content_parts.append(get_file_content(file_path))
                
                content_parts.append(f"\n{separator}")
                content_parts.append(f"END FILE: {relative_path}")
                content_parts.append(f"{separator}\n")
            
            # Write the concatenated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content_parts))
            
            print(f"Created: {output_path} ({len(files)} files)")
            processed_folders.add(current_folder)
        
        # Process subfolders
        for item in sorted(current_folder.iterdir()):
            if item.is_dir() and item.name not in skip_dirs:
                process_folder(item)
    
    # Start processing from the root folder
    process_folder(folder_path)
    
    # Also create a combined file for the entire project (root folder name)
    create_full_project_file(folder_path, output_dir, skip_dirs, include_extensions)


def create_full_project_file(folder_path, output_dir, skip_dirs, include_extensions):
    """Create a single file containing ALL files from the entire project."""
    folder_path = Path(folder_path)
    output_dir = Path(output_dir)
    
    output_filename = f"{folder_path.name}.txt"
    output_path = output_dir / output_filename
    
    content_parts = []
    content_parts.append(f"{'='*60}")
    content_parts.append(f"FULL PROJECT: {folder_path.name}")
    content_parts.append(f"{'='*60}\n")
    
    file_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        # Filter out skip directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        root_path = Path(root)
        
        for filename in sorted(files):
            file_path = root_path / filename
            
            # Check extension
            if file_path.suffix.lower() not in include_extensions and file_path.suffix != '':
                continue
            
            # Get relative path from project root
            relative_path = file_path.relative_to(folder_path)
            separator = "-" * 50
            
            content_parts.append(f"\n{separator}")
            content_parts.append(f"START FILE: {relative_path}")
            content_parts.append(f"{separator}\n")
            
            content_parts.append(get_file_content(file_path))
            
            content_parts.append(f"\n{separator}")
            content_parts.append(f"END FILE: {relative_path}")
            content_parts.append(f"{separator}\n")
            
            file_count += 1
    
    if file_count > 0:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        print(f"\nCreated full project file: {output_path} ({file_count} total files)")


def main():
    parser = argparse.ArgumentParser(
        description='Concatenate files in each folder into single text files with separators.'
    )
    parser.add_argument(
        'input_folder',
        help='Path to the root folder to process'
    )
    parser.add_argument(
        '-o', '--output',
        default='./concatenated_output',
        help='Output directory for concatenated files (default: ./concatenated_output)'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_folder)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_path}' does not exist.")
        return 1
    
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a directory.")
        return 1
    
    print(f"Processing folder: {input_path}")
    print(f"Output directory: {args.output}\n")
    
    concatenate_folder_files(input_path, args.output)
    
    print("\nDone!")
    return 0


if __name__ == '__main__':
    exit(main())
