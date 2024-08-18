import re
from datetime import datetime
import emoji


class UserInputCheck:
    def __init__(self):
        pass

    def get_input(self, prompt):
        while True:
            user_input = input(prompt).lower().strip()
            if user_input in ['y', 'n']:
                return user_input
            print("Sorry, that's not a possible option. Please enter 'Y' or 'N'.")

    def formatted_kinds_activities(self, kinds):
        kinds = kinds.strip()
        kinds = re.sub(r',+', ',', kinds)
        kinds = re.sub(r'\s*,\s*',',', kinds)
        kinds = re.sub(r'\s+', ',', kinds)
        kinds = re.sub(r'[-_+=!?/|;:#*~]', '', kinds)
        kinds = kinds.strip(',')

        return kinds

def valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            if date_obj.date() < datetime.today().date():
                print("The check-in date must be today or later. Please enter a valid date.")
            else:
                new_format_date = date_obj.strftime("%Y-%m-%d")
                return new_format_date
        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format.")

class SavingToFavourites:
    def __init__(self):
        self.favourite_hotels = []
        self.favourite_activities = []

    def save_favourites(self, category, id, name, input_check):
        wants_save = input_check.get_input(f'Would you like to save this {category} in your list of favourites? Y/N ')
        if wants_save == 'y':
            item = {
                f'{category[:-1]} id': id,
                'name': name,
                'added_on': datetime.now().strftime("%Y-%m-%d")
            }

            if category == 'activities':
                self.favourite_activities.append(item)
            elif category == 'hotels':
                self.favourite_hotels.append(item)
            print(emoji.emojize('Consider it done!:thumbs_up:'))
        else:
            print(emoji.emojize('No problem! :thumbs_up:'))
    def save_favourite_hotels(self, hotel_id, hotel_name, input_check):
        self.save_favourites('hotels', hotel_id, hotel_name, input_check)

    def save_favourite_activities(self, xid, activity_name, input_check):
        self.save_favourites('activities', xid, activity_name, input_check)

    def get_favourites(self, category):
        if category == 'activities':
            return self.favourite_activities
        elif category == 'hotels':
            return self.favourite_hotels

