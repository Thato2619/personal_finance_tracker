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
        """Creates the CSV file if it doesn't exist."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls):
        """Collects transaction details and adds a new entry."""
        date = get_date("Enter the transaction date (dd-mm-yyyy) or press Enter for today: ", allow_default=True)
        amount = get_amount()
        category = get_category()
        description = get_description()

        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print("\n✅ Transaction added successfully!\n")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Retrieves transactions within a user-specified date range and prints a summary."""
        try:
            df = pd.read_csv(cls.CSV_FILE)
            if df.empty:
                print("\n❌ No transactions recorded yet.\n")
                return

            df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, errors="coerce")
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

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
            print(income_df.to_string(index=False) if not income_df.empty else "No income transactions recorded.")

            print("\n🔹 **Expense Transactions** 🔹")
            print(expense_df.to_string(index=False) if not expense_df.empty else "No expense transactions recorded.")

            # ✅ Calculate Summary for the Filtered Transactions
            total_income_filtered = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense_filtered = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            # ✅ Calculate Overall Summary (All Transactions)
            total_income_all = df[df["category"] == "Income"]["amount"].sum()
            total_expense_all = df[df["category"] == "Expense"]["amount"].sum()

            # ✅ Print Filtered Summary
            if not filtered_df.empty:
                print(f"\n🔹 **Summary (Filtered: {start_date.strftime(cls.FORMAT)} - {end_date.strftime(cls.FORMAT)})** 🔹")
                print(f"Total Income: ${total_income_filtered:.2f}")
                print(f"Total Expense: ${total_expense_filtered:.2f}")
                print(f"Net Savings: ${(total_income_filtered - total_expense_filtered):.2f}")

            # ✅ Print Overall Summary
            print("\n🔹 **Overall Summary (All Transactions)** 🔹")
            print(f"Total Income (All Time): ${total_income_all:.2f}")
            print(f"Total Expense (All Time): ${total_expense_all:.2f}")
            print(f"Net Savings (All Time): ${(total_income_all - total_expense_all):.2f}")

        except FileNotFoundError:
            print("\n❌ No transaction data found. Please add transactions first.\n")

# ✅ Menu System
def main():
    CSV.initialize_csv()
    
    while True:
        print("\n🔹 **Personal Finance Tracker** 🔹")
        print("1️⃣ Add a Transaction")
        print("2️⃣ View Transactions and Summary")
        print("3️⃣ Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            CSV.add_entry()
        elif choice == "2":
            start_date = get_date("Enter start date (dd-mm-yyyy): ")
            end_date = get_date("Enter end date (dd-mm-yyyy): ")
            CSV.get_transactions(start_date, end_date)
        elif choice == "3":
            print("\n✅ Exiting... Have a great day!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-3.\n")

if __name__ == "__main__":
    main()
