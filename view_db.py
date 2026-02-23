import sqlite3
from tabulate import tabulate

# Connect to database
conn = sqlite3.connect("imageforge.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if not tables:
    print("No tables found.")
else:
    for table in tables:
        table_name = table[0]
        print(f"\n=== Table: {table_name} ===")

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        if rows:
            print(tabulate(rows, headers=column_names, tablefmt="grid"))
        else:
            print("Table is empty.")

conn.close()