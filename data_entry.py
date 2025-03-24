from datetime import datetime


date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

from datetime import datetime

date_format = "%d-%m-%Y"  # Corrected Year Format
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt).strip()

    # Use default date if allowed and user enters nothing
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)  # Ensure output is a string
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy.")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

def get_description():
    return input("Enter a description (optional): ")