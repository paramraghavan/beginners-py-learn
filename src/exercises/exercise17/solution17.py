import os

def process_file(file_path):
    """
    Function to process the file.
    This is a placeholder function and should be replaced with actual processing logic.
    """
    # Simulate processing
    print(f"Processing file: {file_path}")
    # Raise an exception for demonstration purposes
    # Remove or modify this in actual implementation
    if os.path.basename(file_path).startswith("fail"):
        raise Exception("Simulated processing failure")


def process_files_in_folder(folder_path):
    total_files = 0
    success_count = 0
    failure_count = 0

    # Loop through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            total_files += 1
            try:
                process_file(file_path)
                success_count += 1
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
                failure_count += 1

    print(f"Total files: {total_files}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed to process: {failure_count}")


# Example usage
folder_path = '/path/to/your/folder'  # Replace with your folder path
process_files_in_folder(folder_path)
