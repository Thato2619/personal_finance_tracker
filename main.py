import pandas as pd
import csv
import matplotlib.pyplot as plt
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
        """Retrieves transactions, prints the summary, and returns a DataFrame."""
        try:
            df = pd.read_csv(cls.CSV_FILE)
            if df.empty:
                print("\n❌ No transactions recorded yet.\n")
                return pd.DataFrame()

            df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, errors="coerce")
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

            start_date = datetime.strptime(start_date, cls.FORMAT)
            end_date = datetime.strptime(end_date, cls.FORMAT)

            # Filter transactions
            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            # ✅ Print transaction breakdown
            print("\n🔹 **Transaction Breakdown (Filtered Range)** 🔹")
            print(filtered_df.to_string(index=False) if not filtered_df.empty else "No transactions in this range.")

            # ✅ Summary calculations
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            net_savings = total_income - total_expense

            # ✅ Print Summary
            print("\n🔹 **Summary** 🔹")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${net_savings:.2f}")

            return filtered_df  # ✅ Return filtered transactions for graphing

        except FileNotFoundError:
            print("\n❌ No transaction data found. Please add transactions first.\n")
            return pd.DataFrame()

# ✅ Create Graph
def plot_transactions(df):
    if df.empty:
        print("\n❌ No transactions available for graph.\n")
        return

    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")["amount"]
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")["amount"]
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df, label="Income", color="g")
    plt.plot(expense_df.index, expense_df, label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

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
            df = CSV.get_transactions(start_date, end_date)  # ✅ Print summary first

            if not df.empty:
                # ✅ Ask user if they want to see the graph
                show_graph = input("\n📊 Do you want to see a graph? (yes/no): ").strip().lower()
                if show_graph in ["yes", "y"]:
                    plot_transactions(df)  # ✅ Show graph only if user says "yes"
        elif choice == "3":
            print("\n✅ Exiting... Have a great day!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-3.\n")

if __name__ == "__main__":
    main()
