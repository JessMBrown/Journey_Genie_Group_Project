from config import HOST, PASSWORD, USER
from db_utils_oli import Database, DbConnectionError
import emoji
from datetime import datetime


class SavingToFavourites:
    def __init__(self):
        self.favourite_hotels = []
        self.favourite_activities = []

    def save_favourites(self, category, id, name, city_choice, city_id, input_check, chosen_country, country_code):
        wants_save = input_check.get_input(f'Would you like to save this {category} in your list of favourites? Y/N ')
        if wants_save == 'y':
            item = {
                f'{category[:-1]} id': id,
                'name': name,
                'city': city_choice,
                'city_ID': city_id,
                'country': chosen_country,
                'country_code': country_code,
                'added_on': datetime.now().strftime("%Y-%m-%d")
            }

            if category == 'activities':
                self.favourite_activities.append(item)
            elif category == 'hotels':
                self.favourite_hotels.append(item)
            print(emoji.emojize('Consider it done!:thumbs_up:'))
        else:
            print(emoji.emojize('No problem! :thumbs_up:'))


    def save_favourite_hotels(self, hotel_id, hotel_name, city_choice, city_id, input_check, chosen_country, country_code):
        self.save_favourites('hotels', hotel_id, hotel_name, city_choice, city_id, input_check, chosen_country, country_code)

    def save_favourite_activities(self, xid, activity_name, city_choice, city_id, input_check, chosen_country, country_code):
        self.save_favourites('activities', xid, activity_name, city_choice, city_id, input_check, chosen_country, country_code)

    def get_favourites(self, category):
        if category == 'activities':
            return self.favourite_activities
        elif category == 'hotels':
            return self.favourite_hotels



def store_data_in_database(table_name, columns, values):
    db = Database(host=HOST, user=USER, password=PASSWORD, db_name='customer_details')

    try:
        db.add_new_data(
            table_name=table_name,
            columns=columns,
            values=values
        )
    except DbConnectionError as e:
        print(f"Failed to store mail_and_favourites in the database: {e}")

def store_favourites_in_database(user_data, table_name):
    if table_name == 'favourite_hotels':
        columns = ['fav_hotel_ID', 'hotel_name', 'city_ID', 'country_code', 'favourited_date']
        values = (user_data['hotel_id'], user_data['hotel_name'], user_data['city_ID'], user_data['country_code'], user_data['favourited_date'])
    elif table_name == 'favourite_activities':
        columns = ['activity_ID', 'activity_name', 'city_ID', 'country_code', 'favourited_date']
        values = (user_data['activity_ID'], user_data['activity_name'], user_data['city_ID'], user_data['country_code'],
                  user_data['favourited_date'])
    else:
        print('Invalid table')
        return

    store_data_in_database(table_name, columns, values)
