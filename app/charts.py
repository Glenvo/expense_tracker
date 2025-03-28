import matplotlib.pyplot as plt
from .logic import load_expenses_df

def plot_monthly_comparison():
    df = load_expenses_df()
    df["month"] = df["date"].dt.to_period("M")
    summary = df.groupby("month")["amount"].sum()
    summary.plot(kind="bar", title="Monthly Expenses", color="skyblue")
    plt.xlabel("Month")
    plt.ylabel("Total Spent")
    plt.tight_layout()
    plt.show()
