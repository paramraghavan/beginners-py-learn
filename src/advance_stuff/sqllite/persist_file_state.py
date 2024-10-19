import sqlite3
import time

DB_NAME = 'file_status.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_status
    (filename TEXT PRIMARY KEY, status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def add_or_update_file_status(filename, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO file_status (filename, status, timestamp) 
    VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (filename, status))
    conn.commit()
    conn.close()

def get_file_status(filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT status, timestamp FROM file_status WHERE filename = ?', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result if result else ('unknown', None)

def print_all_statuses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT filename, status, timestamp FROM file_status ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()

    print("\nCurrent File Statuses:")
    print("-" * 70)
    for filename, status, timestamp in results:
        print(f"Filename: {filename:<20} Status: {status:<10} Last Updated: {timestamp}")
    print("-" * 70)

if __name__ == "__main__":
    init_db()

    print("File Status Manager")
    print("Commands: add <filename> <status>, get <filename>, list, quit")

    while True:
        command = input("> ").strip().split()
        if not command:
            continue

        if command[0] == "add" and len(command) == 3:
            add_or_update_file_status(command[1], command[2])
            print(f"Added/Updated status for {command[1]}")
        elif command[0] == "get" and len(command) == 2:
            status, timestamp = get_file_status(command[1])
            print(f"Status of {command[1]}: {status} (Last updated: {timestamp})")
        elif command[0] == "list":
            print_all_statuses()
        elif command[0] == "quit":
            break
        else:
            print("Invalid command. Use 'add <filename> <status>', 'get <filename>', 'list', or 'quit'")

    print("File Status Manager stopped.")