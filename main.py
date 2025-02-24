from utils import UserInputCheck, get_valid_dates
import random
from mail_and_favourites.get_favourites import SavingToFavourites
from location.get_location import Location
from mail_and_favourites.get_email import get_email
from config import HOST, PASSWORD, USER
from hotels.get_hotels import get_hotels
from activities.get_activities import find_and_display_activities
from weather.get_weather import find_weather
import emoji

# Creating instances for classes for handling user input, location and favourites
planner = Location(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
input_check = UserInputCheck()
favourites_manager = SavingToFavourites()


# Function to handle the case when the user knows which country he wants to go to
def knows_destination(planner, start_date, end_date):
    try:
        # fetch list of countries from db
        country_list = planner.get_countries()

        # loop to ensure the user enters a valid country
        while True:
            globe = emoji.emojize(":globe_showing_Americas:")
            chosen_country = input(f"Please, enter the name of the country {globe}: ").strip().lower()
            if chosen_country in [country.lower() for country in country_list]:
                # fetch the cities for the chosen country if it's part of the db
                city_choice = planner.get_cities_by_country(chosen_country)
                break
            else:
                print('This country is not part of our holiday destinations! Please try again!')

        # call function that handles the rest of the logic which is the same for each of the 3 options
        plan_trip_details(city_choice, start_date, end_date, chosen_country)

        return city_choice, chosen_country

    except Exception as e:
        print(f'An error occurred: {e}')


# function to tailor a trip based on user preferences
def tailored_trip(planner, start_date, end_date):
    # city/country function to display countries by filters
    city_choice, chosen_country = planner.get_holiday_type_cities()

    # call function that handles the rest of the logic which is the same for each of the 3 options
    plan_trip_details(city_choice, start_date, end_date, chosen_country)
    return chosen_country, city_choice


def take_me_anywhere(planner, start_date, end_date):
    city_choice = None
    random_countries = []
    try:
        # fetch list of available countries from db
        country_list = planner.get_countries()

        while True:
            if not random_countries:
                # randomly selects 5 countries from that list
                random_countries = random.sample(country_list, k=5)

            # creating a variable to store the sample and format it. In case of wrong input it will be displayed again
            display_countries = ', '.join(random_countries)
            # y/n questions are handled with a method in utils to check for correct input
            good_selection = input_check.get_input(f"Fancy any of these countries? \U0001F30E {display_countries} Y/N ")
            if good_selection == 'y':
                # get user input
                chosen_country = input('Please enter the name of the country: ').strip().lower()
                # avoids doubles
                if chosen_country in [country.lower() for country in random_countries]:
                    # call cities for the chosen country if valid
                    city_choice = planner.get_cities_by_country(chosen_country.capitalize())
                    break
            elif good_selection == 'n':
                # if the user is not happy with initial selection a new one is created
                print('No worries! ')
                random_countries = []
                continue
            else:
                print(f'Invalid answer! Please try again: ')

    except Exception as e:
        print(f'An error occurred: {e}')

    if city_choice:
        plan_trip_details(city_choice, start_date, end_date, chosen_country)

    return city_choice, chosen_country


def fetch_and_display_summary(start_date, end_date, saved_hotels, saved_activities, city_choice, chosen_country):
    # list comprehension to make a list of the hotels and activities the user has selected if any
    favourite_hotels = [hotel['name'] for hotel in saved_hotels] if saved_hotels else ['None']
    favourite_activities = [activity['name'] for activity in saved_activities] if saved_activities else ['None']

    summary = (f"\nYour holiday in {city_choice.capitalize()}, {chosen_country.capitalize()} from the {start_date} "
               f"to {end_date}:\n"
               f"Here are the hotels you selected:  {', '.join(favourite_hotels)}. \n"
               f"Here are the activities you selected: {', '.join(favourite_activities)}.\n"
               f"This will be sent to your email if you required it!")

    print(summary)
    return


# function to continue the end of the logic for each option
def plan_trip_details(city_choice, start_date, end_date, chosen_country):
    # call get_weather to get weather prediction displayed
    print("")
    find_weather(city_choice, start_date, end_date)
    print("")
    print(start_date)
    # call get_hotels to get a selection of hotels by filter
    print("Looks great! Now, let's find you a hotel \U0001F3E8")
    saved_hotels = get_hotels(city_choice, start_date, end_date)
    print("")

    # call get_activities to get a selection of activities by filter
    print(f"Let's find you some activities in {city_choice}! \U0001fa84 ")
    saved_activities = find_and_display_activities(city_choice)
    print("")

    # Offer to have information sent by email (is not fully implemented. It currently sends user information to db)
    get_email()

    # display end summary of the choices the user has made
    fetch_and_display_summary(start_date, end_date, saved_hotels, saved_activities, city_choice, chosen_country)

    favourites_manager.store_all_favourites_in_database()


def main():
    # Welcoming user and getting some basic details
    sparkle = emoji.emojize(":sparkles:")
    print(f"Hello! Welcome to {sparkle}Journey Genie{sparkle}!\nLet's start prepping your next holiday")
    #       f" {emoji.emojize(":beach_with_umbrella:")}")
    start_date, end_date = get_valid_dates()

    knows_where = input_check.get_input("Do you know which country you'd like to go to? Y/N ")

    if knows_where == 'y':
        knows_destination(planner, start_date, end_date)
    elif knows_where == 'n':
        wants_random = input_check.get_input("No worries! We're here to help! Would you like us to make a random guess"
                                             " \U0001F52E of a nice holiday place for you? Y/N ")
        if wants_random == 'y':
            take_me_anywhere(planner, start_date, end_date)
        elif wants_random == 'n':
            print("\nOk! Let's tailor a holiday for you!")
            tailored_trip(planner, start_date, end_date)

    print("\nThe Journey Genie has done his magic! \U0001F4AB Now back to the lamp sipping cocktails \U0001F379 "
          "until you need him again!")


if __name__ == "__main__":
    main()
