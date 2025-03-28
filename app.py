from app.db import init_db
from app.models import add_expense
from app.logic import get_monthly_summary
from app.charts import plot_monthly_comparison

def main():
    init_db()

    # sample
    add_expense("Food", 20.0, "Lunch")
    add_expense("Transport", 15.5, "Bus", "2025-03-01")

    total, df = get_monthly_summary(2025, 3)
    print(f"Total spent in March 2025: ${total:.2f}")
    print(df)

    plot_monthly_comparison()

if __name__ == "__main__":
    main()
