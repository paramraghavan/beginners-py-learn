import os
import subprocess
from datetime import datetime
import sys
from typing import List, Tuple


def find_run_files(directory: str) -> List[str]:
    """
    Find all Python files starting with 'run' in the specified directory
    """
    run_files = []
    try:
        for file in os.listdir(directory):
            if file.startswith('run') and file.endswith('.py'):
                run_files.append(os.path.join(directory, file))
        return sorted(run_files)  # Sort files for consistent execution order
    except Exception as e:
        print(f"Error searching directory: {str(e)}")
        return []


def execute_python_file(file_path: str) -> Tuple[str, int, str]:
    """
    Execute a Python file and return its output

    Returns:
        Tuple containing (output, return_code, error_message)
    """
    try:
        # Execute the Python file and capture output
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return (result.stdout, result.returncode, result.stderr)
    except subprocess.TimeoutExpired:
        return ("", 1, f"Execution timed out after 5 minutes")
    except Exception as e:
        return ("", 1, f"Error executing file: {str(e)}")


def save_output(output_file: str, content: str, return_code: int, error_msg: str) -> None:
    """
    Save the execution output to a file with timestamp and status
    """
    try:
        with open(output_file, 'w') as f:
            f.write(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Status: {'Success' if return_code == 0 else 'Failed'}\n")
            f.write("=" * 50 + "\n")

            if content.strip():
                f.write("OUTPUT:\n")
                f.write(content)
                f.write("\n")

            if error_msg.strip():
                f.write("ERRORS:\n")
                f.write(error_msg)
    except Exception as e:
        print(f"Error saving output to {output_file}: {str(e)}")


def main(directory: str = ".") -> None:
    """
    Main function to process all run*.py files
    """
    # Find all run*.py files
    run_files = find_run_files(directory)

    if not run_files:
        print(f"No Python files starting with 'run' found in {directory}")
        return

    print(f"Found {len(run_files)} files to execute")

    # Process each file
    for file_path in run_files:
        file_name = os.path.basename(file_path)
        output_file = os.path.splitext(file_path)[0] + '_output.txt'

        print(f"\nProcessing: {file_name}")
        print(f"Output will be saved to: {output_file}")

        # Execute the file
        output, return_code, error_msg = execute_python_file(file_path)

        # Save the output
        save_output(output_file, output, return_code, error_msg)

        # Print status
        status = "Success" if return_code == 0 else "Failed"
        print(f"Execution {status}")
        if error_msg.strip():
            print(f"Errors encountered: {error_msg.strip()}")

"""
# To process files in current directory
python execute_run_files.py

# To process files in a specific directory
python execute_run_files.py /path/to/your/directory
"""

if __name__ == "__main__":
    # Use current directory by default, or accept directory as command line argument
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    main(directory)
