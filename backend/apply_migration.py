#!/usr/bin/env python3
"""Script to apply database migrations"""

import sqlite3
import os


def apply_migration():
    db_path = "test.db"
    migration_path = "migrations/update_schema.sql"

    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        print("Please run create_db.py first to create the database")
        return False

    if not os.path.exists(migration_path):
        print(f"Migration file not found: {migration_path}")
        return False

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)

        # Read and execute the migration
        with open(migration_path, "r", encoding="utf-8") as f:
            migration_sql = f.read()

        # Execute the changes
        conn.executescript(migration_sql)
        conn.commit()
        conn.close()

        print("✅ Migration applied successfully!")
        return True

    except Exception as e:
        print(f"❌ Error applying migration: {e}")
        return False


if __name__ == "__main__":
    apply_migration()
