import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_description, get_date

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print("Entry added successfully.")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            df = pd.read_csv(cls.CSV_FILE)  # Load CSV data
            if df.empty:
                print("No transactions recorded yet.")
                return

            # Convert date column to datetime
            df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, errors="coerce")
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  # Ensure numeric values

            # Convert input dates to datetime
            start_date = datetime.strptime(start_date, cls.FORMAT)
            end_date = datetime.strptime(end_date, cls.FORMAT)

            # Apply filtering
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            # ✅ Print All Transactions Breakdown
            print("\n🔹 **Transaction Breakdown (All Records)** 🔹\n")
            print(df.to_string(index=False))

            # ✅ Group transactions by category
            income_df = df[df["category"] == "Income"]
            expense_df = df[df["category"] == "Expense"]

            # ✅ Print transactions by category
            print("\n🔹 **Income Transactions** 🔹")
            if income_df.empty:
                print("No income transactions recorded.")
            else:
                print(income_df.to_string(index=False))

            print("\n🔹 **Expense Transactions** 🔹")
            if expense_df.empty:
                print("No expense transactions recorded.")
            else:
                print(expense_df.to_string(index=False))

            # ✅ Calculate Summary for the Filtered Transactions
            total_income_filtered = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense_filtered = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            # ✅ Calculate Overall Summary (All Transactions)
            total_income_all = df[df["category"] == "Income"]["amount"].sum()
            total_expense_all = df[df["category"] == "Expense"]["amount"].sum()

            # ✅ Print Filtered Summary
            if not filtered_df.empty:
                print(f"\n🔹 **Summary (Filtered Range: {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)})** 🔹")
                print(f"Total Income: ${total_income_filtered:.2f}")
                print(f"Total Expense: ${total_expense_filtered:.2f}")
                print(f"Net Savings: ${(total_income_filtered - total_expense_filtered):.2f}")

            # ✅ Print Overall Summary
            print("\n🔹 **Overall Summary (All Transactions)** 🔹")
            print(f"Total Income (All Time): ${total_income_all:.2f}")
            print(f"Total Expense (All Time): ${total_expense_all:.2f}")
            print(f"Net Savings (All Time): ${(total_income_all - total_expense_all):.2f}")

        except FileNotFoundError:
            print("No transaction data found. Please add transactions first.")

# ✅ Run this to test
CSV.get_transactions("01-02-2024", "20-02-2024")
