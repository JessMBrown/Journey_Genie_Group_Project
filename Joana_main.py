from utils import UserInputCheck, get_valid_dates, SavingToFavourites, state
import random
from location.get_location import Location
from email.get_email import get_email
from config import HOST, PASSWORD, USER
from hotels.get_hotels import find_hotels
from activities.get_activities import get_activities, get_activity_details
# from weather.get_weather import find_weather

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
                print('Invalid answer!')

        state.chosen_country = chosen_country

        end_of_function_planning(city_choice, start_date, end_date)

        return chosen_country, city_choice

    except Exception as e:
        print(f'An error occurred: {e}')


# def tailored_trip(planner, start_date, end_date):
#     # # city/country function to display countries based on what user is looking for
#     while True:
#         planner.get_holiday_type_input()
#         planner.get_holiday_type_cities()
#         # is_interested = input_check.get_input("Does any of these city interest you? Y/N ")
#         # if is_interested == 'y':
#         #     city_choice = input("Please enter the number corresponding to the city you want to select: ")
#         break
#
#
#     end_of_function_planning(city_choice, start_date, end_date)
#     return chosen_country

def take_me_anywhere(planner, start_date, end_date):
    try:
        #  create code to randomly call a country
        country_list = planner.get_countries()

        while True:
            random_countries = random.sample(country_list, k=5)
            good_selection = input(f"Fancy any of these countries? {random_countries} Y/N ").lower().strip()
            if good_selection == 'y':
                chosen_country = input('Please enter the name of the country: ').strip().lower()
                if chosen_country in [country.lower() for country in random_countries]:
                    # call cities
                    city_choice = planner.get_cities_by_country(chosen_country.capitalize())
                    break
            elif good_selection == 'n':
                print('No worries! ')
                continue
            else:
                print('Invalid answer! Please type Y or N ')

        state.chosen_country = chosen_country

        end_of_function_planning(city_choice, start_date, end_date)

        return chosen_country

    except Exception as e:
        print(f'An error occurred: {e}')



def end_of_function_planning(city_choice, start_date, end_date):
    # # call weather
    # avg_weather_in_city_choice = (
    # find_weather(city_choice, start_date, end_date)
    # print(f"The weather last year at the same dates in {city_choice} was an average of {avg_weather_in_city_choice}")

    # call hotels
    print("Great choice! Now, let's find you a hotel! ")
    find_hotels(city_choice, start_date, end_date)

    # # call activities
    print(f"Let's find you some activities in {city_choice}! ")
    final_results, results = get_activities(city_choice)
    if final_results:
        get_activity_details(final_results, results, city_choice)

    # call email
    get_email()

    #retrieve list of favourites
    print(favourites_manager.get_favourites('activities'))
    print(favourites_manager.get_favourites('hotels'))


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

