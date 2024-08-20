from datetime import datetime

# function to validate the check-in and check-out dates
def get_valid_dates():
    # today's date
    today = datetime.today()

    # calculation to find maximum check-in date (1 year and 1 month ahead)
    max_year = today.year + 1
    max_month = today.month + 1
    if max_month > 12:
        max_month = 1
        max_year += 1

    max_check_in_date = today.replace(year=max_year, month=max_month)

    check_in_date = None
    check_out_date = None
    valid_check_in_date = False
    valid_check_out_date = False

    # check-in date
    while not valid_check_in_date:
        check_in_date_str = input("Enter check-in date (dd-mm-yyyy): ")
        try:
            check_in_date = datetime.strptime(check_in_date_str, "%d-%m-%Y")

            # making sure user does not write a date in the past
            if check_in_date.date() < today.date():
                print("The check-in date must be today or later. Please enter a valid date.")
                continue

            # making sure check in date is within the max
            if check_in_date > max_check_in_date:
                print(
                    "The check-in date cannot be later than one year and one month from today. "
                    "Please enter a valid date.")
                continue

            valid_check_in_date = True
        except ValueError:
            print("Invalid check-in date format. Please enter the date in dd-mm-yyyy format.")

    # get and validate check-out date
    while not valid_check_out_date:
        check_out_date_str = input("Enter check-out date (dd-mm-yyyy): ")
        try:
            check_out_date = datetime.strptime(check_out_date_str, "%d-%m-%Y")

            # making sure check-out date is after the check-in date
            if check_out_date.date() <= check_in_date.date():
                print("Check-out date must be after the check-in date. Please enter the dates again.")
                continue

            valid_check_out_date = True
        except ValueError:
            print("Invalid check-out date format. Please enter the date in dd-mm-yyyy format.")

    return check_in_date, check_out_date
