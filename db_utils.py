from datetime import datetime

# changing datetime output so it's in DD-MM-YYYY format and ensuring date is from today onwards
def valid_date(prompt):
    date_str = input(prompt)
    try:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        if date_obj.date() < datetime.today().date():
            print("The check-in date must be today or later. Please enter a valid date.")
        else:
            return date_obj
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
