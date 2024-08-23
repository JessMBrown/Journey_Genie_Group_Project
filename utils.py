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


def get_valid_dates():
    while True:
        try:
            # today's date
            today = datetime.today().date()

            # calculation to find maximum check-in date (1 year and 1 month ahead)
            max_year = today.year + 1
            max_month = today.month + 1
            if max_month > 12:
                max_month = 1
                max_year += 1

            max_start_date = today.replace(year=max_year, month=max_month)

            start_date_str = input("When would you like your holiday to start? (dd-mm-yyyy): ")
            start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()


            # making sure user does not write a date in the past
            if start_date < today:
                print("The check-in date must be today or later. Please enter a valid date.")
                continue

            # making sure check in date is within the max
            if start_date > max_start_date:
                print(
                    "The check-in date cannot be later than one year and one month from today. Please enter a valid date.")
                continue

            end_date_str = input("When would you like your holiday to end? (dd-mm-yyyy): ")
            end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()

            # making sure check-out date is after the check-in date
            if end_date <= start_date:
                print("Check-out date must be after the check-in date. Please enter the dates again.")
                continue

            return start_date, end_date

        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format.")


def fetch_and_display_summary(start_date, end_date, saved_hotels, saved_activities):
    favourite_hotels = []
    favourite_activities= []
    cities = []
    countries = []
    for hotel in saved_hotels:
        favourite_hotels.append(hotel['name'])
        cities.append(hotel['city'])
        countries.append(hotel['country'])

    for activity in saved_activities:
        favourite_activities.append(activity['name'])

    location_str = ', '.join(f'{city}, {country}' for city, country in zip(cities, countries))


    summary = (f"For your holiday in {location_str} from the {start_date} to {end_date},\nyou have selected "
            f"the hotel(s): {', '.join(favourite_hotels)}. \nYou also selected the activity(ies): {', '.join(favourite_activities)}. "
            f"\nThis will be sent to your email if you required it!")

    print(summary)
    return summary