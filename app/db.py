import sqlite3
import os

DB_PATH = os.path.join("data", "expenses.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs("data", exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            );
        """)
        conn.commit()
