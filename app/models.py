from .db import get_connection
from datetime import datetime

def add_expense(category, amount, description="", date=None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        """, (date, category, amount, description))
        conn.commit()

def get_all_expenses():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        return cursor.fetchall()
