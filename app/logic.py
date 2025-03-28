import pandas as pd
from .models import get_all_expenses

def load_expenses_df():
    data = get_all_expenses()
    df = pd.DataFrame(data, columns=["id", "date", "category", "amount", "description"])
    df["date"] = pd.to_datetime(df["date"])
    return df

def get_monthly_summary(year, month):
    df = load_expenses_df()
    df = df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]
    total = df["amount"].sum()
    return total, df
