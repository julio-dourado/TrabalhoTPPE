#!/usr/bin/env python3
"""Script to create the database from scratch"""

import sqlite3
import os


def create_database():
    db_path = "test.db"
    schema_path = "migrations/create_schema.sql"

    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Existing database removed: {db_path}")

    if not os.path.exists(schema_path):
        print(f"Schema file not found: {schema_path}")
        return False

    try:
        # Connect to the database (it will be created automatically)
        conn = sqlite3.connect(db_path)

        # Read and execute the schema
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # Execute the changes
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()

        print("✅ Database created successfully!")
        return True

    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False


if __name__ == "__main__":
    create_database()
