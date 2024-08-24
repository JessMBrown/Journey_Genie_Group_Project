from database.config_oli import HOST, PASSWORD, USER
from database.db_utils_oli import Database, DbConnectionError
import emoji
from datetime import datetime
import re

class UserInputCheck:
    def __init__(self):
        pass

    def get_input(self, prompt):
        while True:
            user_input = input(prompt).lower().strip()
            if user_input in ['y', 'n']:
                return user_input
            print("Sorry, that's not a possible option. Please enter 'Y' or 'N'.")


class SavingToFavourites:
    def __init__(self):
        self.favourite_hotels = []
        self.favourite_activities = []

    def save_favourite_activities(self, activities, input_check):
        """Accepts a list of activity dictionaries and saves each one."""
        for activity in activities:
            self.save_favourites(
                category='activities',
                id=activity['activity id'],
                name=activity['name'],
                city_choice=activity['city'],
                city_id=activity['city_ID'],
                input_check=input_check,
                chosen_country=activity['country'],
                country_code=activity['country_code']
            )

    def save_favourite_hotels(self, hotels, input_check):
        """Accepts a list of hotel dictionaries and saves each one."""
        for hotel in hotels:
            self.save_favourites(
                category='hotels',
                id=hotel['hotel id'],
                name=hotel['name'],
                city_choice=hotel['city'],
                city_id=hotel['city_ID'],
                input_check=input_check,
                chosen_country=hotel['country'],
                country_code=hotel['country_code']
            )

    def get_favourites(self, category):
        if category == 'activities':
            return self.favourite_activities
        elif category == 'hotels':
            return self.favourite_hotels

    def save_favourites(self, category, id, name, city_choice, city_id, input_check, chosen_country, country_code):
        wants_save = input_check.get_input(f'Would you like to save this {category} in your list of favourites? Y/N ')
        if wants_save.lower() == 'y':
            item = {
                f'{category[:-1]} id': id,
                'name': name,
                'city': city_choice,
                'city_ID': city_id,
                'country': chosen_country,
                'country_code': country_code,
                'added_on': datetime.now().strftime("%Y-%m-%d")
            }

            # Add to appropriate list
            if category == 'activities':
                self.favourite_activities.append(item)
                table_name = 'favourite_activities'
            elif category == 'hotels':
                self.favourite_hotels.append(item)
                table_name = 'favourite_hotels'

            # Attempt to store in the database
            try:
                self.store_favourites_in_database(item, table_name)  # Corrected to self.store_favourites_in_database
                print(emoji.emojize('Consider it done!:thumbs_up:'))
            except Exception as e:
                print(f"Failed to store data in the database: {e}")
        else:
            print(emoji.emojize('No problem! :thumbs_up:'))

    def store_favourites_in_database(self, user_data, table_name):
        if table_name == 'favourite_hotels':
            columns = ['fav_hotel_ID', 'hotel_name', 'city_ID', 'country_code', 'favourite_date']
            values = (
                user_data['hotel id'], user_data['name'], user_data['city_ID'],
                user_data['country_code'], user_data['added_on']
            )
        elif table_name == 'favourite_activities':
            columns = ['activity_ID', 'activity_name', 'city_ID', 'country_code', 'favourite_date']
            values = (
                user_data['activitie id'], user_data['name'], user_data['city_ID'],
                user_data['country_code'], user_data['added_on']
            )
        else:
            print('Invalid table')
            return
        self.store_data_in_database(table_name, columns, values)

    def store_data_in_database(self, table_name, columns, values):
        db = Database(host=HOST, user=USER, password=PASSWORD, db_name='destinations')

        try:
            db.add_new_data(
                table_name=table_name,
                columns=columns,
                values=values
            )
        except DbConnectionError as e:
            print(f"Failed to store data in the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    input_check = UserInputCheck()
    fav_manager = SavingToFavourites()

# Example of saving a favourite hotel
# fav_manager.save_favourite_hotels(284601, 'Ateneo Puerta del Sol', 'Madrid', '123484', input_check, 'Spain', 'es')

# Example of saving a favourite activity
# fav_manager.save_favourite_activities('N6220668933', 'Campo dos Mártires da Pátria', 'Lisbon', '123689', input_check,
# 'Portugal', 'pt')

# hotels = [
#     {'hotel id': 331978, 'name': 'Four Seasons Hotel Ritz Lisbon', 'city': 'Lisbon', 'city_ID': '123689',
#      'country': 'Portugal', 'country_code': 'pt', 'added_on': '2024-08-24'},
#     {'hotel id': 7955, 'name': 'Olissippo Lapa Palace – The Leading Hotels of the World', 'city': 'Lisbon',
#      'city_ID': '123689', 'country': 'Portugal', 'country_code': 'pt', 'added_on': '2024-08-24'}
# ]
#
# fav_manager.save_favourite_hotels(hotels, input_check)

activities = [
        {'activity id': 'd112233', 'name': 'City Tour', 'city': 'Lisbon', 'city_ID': '123689', 'country': 'Portugal', 'country_code': 'pt', 'added_on': '2024-08-24'},
        {'activity id': '44f5566', 'name': 'River Cruise', 'city': 'Lisbon', 'city_ID': '123689', 'country': 'Portugal', 'country_code': 'pt', 'added_on': '2024-08-24'}
    ]

# Call the function to save multiple activities
fav_manager.save_favourite_activities(activities, input_check)