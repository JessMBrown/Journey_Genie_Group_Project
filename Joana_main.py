from utils import UserInputCheck, get_valid_dates, fetch_and_display_summary
import random
from mail_and_favourites.get_favourites import SavingToFavourites, store_favourites_in_database
from location.get_location import Location
from mail_and_favourites.get_email import get_email
from config_joana import HOST, PASSWORD, USER
from hotels.get_hotels import get_hotels
from activities.get_activities import find_and_display_activities
from weather.get_weather import find_weather

planner = Location(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
input_check = UserInputCheck()
favourites_manager = SavingToFavourites()


def knows_destination(planner, start_date, end_date):
    try:
        country_list = planner.get_countries()
        while True:
            chosen_country = input("Please, enter the name of the country: ").strip().lower()
            if chosen_country in [country.lower() for country in country_list]:
                city_choice = planner.get_cities_by_country(chosen_country)
                break
            else:
                print('This country is not part of our holiday destinations! Please try again!')

        end_of_function_planning(city_choice, start_date, end_date)

        return city_choice

    except Exception as e:
        print(f'An error occurred: {e}')


def tailored_trip(planner, start_date, end_date):
    # city/country function to display countries based on what user is looking for
    city_choice, chosen_country = planner.get_holiday_type_cities()

    end_of_function_planning(city_choice, start_date, end_date)
    return chosen_country, city_choice

def take_me_anywhere(planner, start_date, end_date):
    city_choice = None
    random_countries = []
    try:
        #  create code to randomly call a country
        country_list = planner.get_countries()

        while True:
            if not random_countries:
                random_countries = random.sample(country_list, k=5)

            # creating a variable to store the sample and format it. In case a wrong input it will be displayed again
            display_countries = ', '.join(random_countries)
            good_selection = input(f"Fancy any of these countries? {display_countries} Y/N ").lower().strip()
            if good_selection == 'y':
                chosen_country = input('Please enter the name of the country: ').strip().lower()
                if chosen_country in [country.lower() for country in random_countries]:
                    # call cities
                    city_choice = planner.get_cities_by_country(chosen_country.capitalize())
                    break
            elif good_selection == 'n':
                print('No worries! ')
                random_countries = []
                continue
            else:
                print(f'Invalid answer! Please try again: ')

    except Exception as e:
        print(f'An error occurred: {e}')

    if city_choice:
        end_of_function_planning(city_choice, start_date, end_date)

    return city_choice


def end_of_function_planning(city_choice, start_date, end_date):
    # # call weather
    find_weather(city_choice, start_date, end_date)

    # call hotels
    print("Looks great! Now, let's find you a hotel! ")
    saved_hotels = get_hotels(city_choice, start_date, end_date)

    # # call activities
    print(f"Let's find you some activities in {city_choice}! ")
    saved_activities = find_and_display_activities(city_choice)

    # call mail and send favourites to db
    get_email()

    #display end summary
    fetch_and_display_summary(start_date, end_date, saved_hotels, saved_activities)
    print(saved_hotels)
    print(saved_activities)

    # store_favourites_in_database(saved_hotels, 'favourite_hotels')
    # store_favourites_in_database(saved_activities, 'favourite_activities')


def main():
    input_check = UserInputCheck()
    # Welcoming user and getting some basic details
    print("Hello! Welcome to Journey Genie! Let's start prepping your next holiday!")
    start_date, end_date = get_valid_dates()

    knows_where = input_check.get_input("Do you know which country you'd like to go to? Y/N ")

    if knows_where == 'y':
        knows_destination(planner, start_date, end_date)
    elif knows_where == 'n':
        wants_random = input_check.get_input("No worries! We're here to help! Would you like us to make a random guess of a nice holiday place for you? Y/N ")
        if wants_random == 'y':
            take_me_anywhere(planner, start_date, end_date)
        elif wants_random == 'n':
            print("Ok! Let's tailor a holiday for you!")
            tailored_trip(planner, start_date, end_date)



if __name__ == "__main__":
    main()

