from database.connection import get_connection

with get_connection() as conn:
    cursor = conn.cursor()

    # List all tables
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    print("Tables:")
    for table in cursor.fetchall():
        print("-", table["name"])

    # Count indexed files
    cursor.execute("SELECT COUNT(*) FROM files")

    count = cursor.fetchone()[0]

    print(f"\nFiles Indexed: {count}")