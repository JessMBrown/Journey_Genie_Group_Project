import re
from datetime import datetime
import emoji

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
                new_format_date = date_obj.strftime("%Y-%m-%d")
                return new_format_date
        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format.")

def save_favourite_activities(favourite_activities, xid, activity_name, input_check):
    wants_save = input_check.get_input('Would you like to save this activity in your list of favourites? Y/N ')
    if wants_save == 'y':
        activity = {
            'activity id': xid,
            'name': activity_name,
            'added_on': datetime.now().strftime("%Y-%m-%d")
        }
        favourite_activities.append(activity)
    print(emoji.emojize('Consider it done!:thumbs_up:'))

def save_favourite_hotels(favourite_hotels, hotel_id, hotel_name, input_check):
    wants_save = input_check.get_input('Would you like to save this hotel in your list of favourites? Y/N ')
    if wants_save == 'y':
        hotel = {
            'hotel id': hotel_id,
            'name': hotel_name,
            'added_on': datetime.now().strftime("%Y-%m-%d")
        }
        favourite_hotels.append(hotel)
    print(emoji.emojize('Consider it done!:thumbs_up:'))
