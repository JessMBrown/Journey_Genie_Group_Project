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

    def save_favourite_activities(self, xid, activity_name, city_choice, city_id, input_check, chosen_country,
                                  country_code):
        self.save_favourites('activities', xid, activity_name, city_choice, city_id, input_check,
                             chosen_country, country_code)

    def save_favourite_hotels(self, hotel_id, hotel_name, city_choice, city_id, input_check, chosen_country,
                              country_code):
        self.save_favourites('hotels', hotel_id, hotel_name, city_choice, city_id, input_check,
                             chosen_country, country_code)

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

            # Adding to appropriate list
            if category == 'activities':
                self.favourite_activities.append(item)
                table_name = 'favourite_activities'
            elif category == 'hotels':
                self.favourite_hotels.append(item)
                table_name = 'favourite_hotels'

            # Attempt to store in the database
            try:
                self.store_favourites_in_database(item, table_name)
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

