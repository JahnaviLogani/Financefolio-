import pandas as pd
import os

FILE = "expenses.csv"

def load_data():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    else:
        return pd.DataFrame(columns=["Date","Category","Description","Amount"])

def save_expense(date, category, description, amount):

    df = load_data()

    new_data = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount
    }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    df.to_csv(FILE,index=False)