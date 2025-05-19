import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os
from app.database import get_db_connection

load_dotenv()

def run_migration_script(name: str, path: str):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS migration_versions (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) UNIQUE NOT NULL,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cur.execute("SELECT 1 FROM migration_versions WHERE name = %s", (name,))
                if cur.fetchone():
                    print(f"Migration '{name}' already applied.")
                    return

                with open(path, "r") as sql_file:
                    cur.execute(sql_file.read())

                cur.execute("INSERT INTO migration_versions (name) VALUES (%s)", (name,))
                conn.commit()
                print(f"Migration '{name}' applied successfully.")
    except Exception as e:
        print(f"Failed to apply migration '{name}': {e}")

def run_all_migrations():
    run_migration_script("create_schema", "scripts/create_schema.sql")
    run_migration_script("insert_demo_data", "scripts/insert_demo_data.sql")
