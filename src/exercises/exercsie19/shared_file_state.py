import sqlite3
import time

DB_NAME = 'file_status.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_status
    (filename TEXT PRIMARY KEY, status TEXT)
    ''')
    conn.commit()
    conn.close()


def add_file_status(filename, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO file_status (filename, status) VALUES (?, ?)',
                   (filename, status))
    conn.commit()
    conn.close()


def update_file_status(filename, status):
    add_file_status(filename, status)  # Same as add in SQLite


def get_file_status(filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM file_status WHERE filename = ?', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'unknown'


def print_complete_status():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM file_status')
    results = cursor.fetchall()
    conn.close()

    print(80 * '*')
    for filename, status in results:
        print(f"Filename: {filename}, Status: {status}")
    print(80 * '*')


if __name__ == "__main__":
    init_db()

    # Initialize with some tasks
    add_file_status('1', "open")
    add_file_status('2', "open")

    print_complete_status()

    print("\nShared task manager is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nShared task manager stopped.")