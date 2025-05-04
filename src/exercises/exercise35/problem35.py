import os
import re

def clean_name(name):
    """Replace spaces, parentheses with underscores in a filename or directory name."""
    # Replace spaces, '(', and ')' with underscores
    return re.sub(r'[ ()]', '_', name)

def remove_empty_folders(path):
    """Remove empty folders recursively."""
    # Check if the path exists
    if not os.path.isdir(path):
        return

    # List all items in the directory
    items = os.listdir(path)

    # If directory is empty, remove it
    if len(items) == 0:
        print(f"Removing empty directory: {path}")
        os.rmdir(path)
        return

    # Check all subdirectories
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            # First process subdirectories recursively
            remove_empty_folders(item_path)

def clean_filesystem(directory):
    """
    Traverse directory structure, rename files and folders that contain spaces
    or parentheses, and remove empty folders.
    """
    # Process all directories first, from deepest to shallowest
    for root, dirs, files in os.walk(directory, topdown=False):
        # First rename files in the current directory
        for file in files:
            if any(c in file for c in ' ()'):
                old_path = os.path.join(root, file)
                new_name = clean_name(file)
                new_path = os.path.join(root, new_name)

                try:
                    print(f"Renaming file: {old_path} -> {new_path}")
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"Error renaming file {old_path}: {e}")

        # Then rename directories
        for dir_name in dirs:
            if any(c in dir_name for c in ' ()'):
                old_path = os.path.join(root, dir_name)
                new_name = clean_name(dir_name)
                new_path = os.path.join(root, new_name)

                try:
                    print(f"Renaming directory: {old_path} -> {new_path}")
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"Error renaming directory {old_path}: {e}")

    # Now remove empty directories
    remove_empty_folders(directory)

if __name__ == "__main__":
    """
        mount
        diskutil list
        diskutil partitionDisk /dev/disk2 MBR FAT32 MUSIC 32G free unused 0B
    """
    import sys

    if len(sys.argv) != 2:
        print("Usage: python rename_script.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(f"Error: {target_directory} is not a valid directory")
        sys.exit(1)

    print(f"Processing directory: {target_directory}")
    clean_filesystem(target_directory)
    print("Done!")