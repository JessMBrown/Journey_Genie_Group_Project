import re
from datetime import datetime

class UserInputCheck:
    def __init__(self):
        pass

    def get_input(self, prompt):
        while True:
            user_input = input(prompt).lower()
            if user_input in ['y', 'n']:
                return user_input
            print("Sorry, that's not a possible option. Please enter 'Y' or 'N'.")
    def formatted_kinds_activities(self, kinds):
        kinds = kinds.strip()
        kinds = re.sub(r',+', ',', kinds)
        kinds = re.sub(r'\s*,\s*',',', kinds)
        kinds = re.sub(r'\s+', ',', kinds)
        kinds = kinds.strip(',')

        return kinds

def valid_date(prompt):
    date_str = input(prompt)
    while True:
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            if date_obj.date() < datetime.today().date():
                print("The check-in date must be today or later. Please enter a valid date.")
            else:
                return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format.")

