from datetime import datetime

date_format = "%d-%m-Y"

def get_date(prompt, allow_default=False):
    date_str =input(prompt)
    if allow_default and not date_format:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy")
        return get_date(prompt, allow_default)