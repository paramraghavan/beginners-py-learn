import re
from datetime import datetime
import os


def extract_sql_statements(log_file_path, output_file=None):
    """
    Extract SQL statements from a log file.

    Args:
        log_file_path (str): Path to the log file
        output_file (str, optional): Path to save extracted SQL statements.
                                   If None, prints to console.

    Returns:
        list: List of dictionaries containing SQL statements and metadata
    """
    # Common SQL keywords to help identify SQL statements
    sql_keywords = r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|MERGE|TRUNCATE|BEGIN|COMMIT|ROLLBACK)\b'

    # Regular expression pattern to match SQL statements
    # This pattern looks for SQL keywords followed by text until a semicolon or new line
    sql_pattern = f"({sql_keywords}.*?)(;|\n)"

    # Store extracted statements with metadata
    extracted_statements = []

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Find all matches in the content
            matches = re.finditer(sql_pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)

            for match in matches:
                sql_statement = match.group(1).strip()

                # Skip if the statement is too short (likely a false positive)
                if len(sql_statement) < 10:
                    continue

                # Try to extract timestamp if it exists in the line
                timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',
                                            match.string[:match.start()])
                timestamp = timestamp_match.group(0) if timestamp_match else None

                statement_info = {
                    'timestamp': timestamp,
                    'statement': sql_statement,
                    'type': re.match(sql_keywords, sql_statement, re.IGNORECASE).group(0).upper()
                }

                extracted_statements.append(statement_info)

        # Write to output file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"SQL Statements Extracted from {os.path.basename(log_file_path)}\n")
                f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                for stmt in extracted_statements:
                    f.write("-" * 80 + "\n")
                    if stmt['timestamp']:
                        f.write(f"Timestamp: {stmt['timestamp']}\n")
                    f.write(f"Type: {stmt['type']}\n")
                    f.write("Statement:\n")
                    f.write(f"{stmt['statement']}\n\n")

        return extracted_statements

    except FileNotFoundError:
        print(f"Error: File {log_file_path} not found")
        return []
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return []


def analyze_sql_statements(statements):
    """
    Analyze the extracted SQL statements and provide basic statistics.

    Args:
        statements (list): List of dictionaries containing SQL statements

    Returns:
        dict: Statistics about the SQL statements
    """
    stats = {
        'total_statements': len(statements),
        'by_type': {},
        'avg_length': 0,
        'time_range': {'start': None, 'end': None}
    }

    total_length = 0
    timestamps = []

    for stmt in statements:
        # Count by type
        stmt_type = stmt['type']
        stats['by_type'][stmt_type] = stats['by_type'].get(stmt_type, 0) + 1

        # Calculate length
        total_length += len(stmt['statement'])

        # Track timestamps
        if stmt['timestamp']:
            timestamps.append(datetime.strptime(stmt['timestamp'], '%Y-%m-%d %H:%M:%S'))

    if statements:
        stats['avg_length'] = total_length / len(statements)

    if timestamps:
        stats['time_range']['start'] = min(timestamps)
        stats['time_range']['end'] = max(timestamps)

    return stats


# Example usage
if __name__ == "__main__":
    # Example log file path
    log_file = "database.log"
    output_file = "extracted_sql.txt"

    # Extract SQL statements
    statements = extract_sql_statements(log_file, output_file)

    # Analyze the statements
    stats = analyze_sql_statements(statements)

    # Print statistics
    print("\nSQL Statement Analysis:")
    print(f"Total statements found: {stats['total_statements']}")
    print("\nStatements by type:")
    for stmt_type, count in stats['by_type'].items():
        print(f"  {stmt_type}: {count}")
    print(f"\nAverage statement length: {stats['avg_length']:.2f} characters")

    if stats['time_range']['start']:
        print(f"\nTime range:")
        print(f"  Start: {stats['time_range']['start']}")
        print(f"  End: {stats['time_range']['end']}")
