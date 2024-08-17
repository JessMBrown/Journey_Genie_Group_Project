from utils import UserInputCheck, valid_date
import random
from activities.get_activities import get_activities
from get_location import Location
from Config import HOST, PASSWORD, USER
from get_hotels import find_hotels
from activities.get_activities import get_activities, get_activity_details

planner = Location(host=HOST, user=USER, password=PASSWORD, db_name='destinations')
input_check = UserInputCheck()


# def knows_destination(): # KAREN
#     chosen_country = input("Please, enter the name of the country: ").strip().capitalize()  # modify to make it a fixed list of countries
#     planner.get_cities_by_country(chosen_country)
#     #  Call weather
#     #  call hotels function to get list of hotels
#     #  call activities function to make suggestions find_activities(city)
#     #  call email function
#
#
# def tailored_trip(planner): # JOANA
#     # # city/country function to display countries based on what user is looking for
#     # country_choice = find_cities(preferences)
#     # city_choice = find_cities(country_choice)
#     # # call weather
#     # find_weather(city_choice, start_date, end_date)
#     # # call hotels
#     # find_hotels(city_choice, start_date, end_date, num_adults, num_children)
#     # # call activities
#     # get_activities(city_choice)
#     # # call email
#     # get_email()
#     pass

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

    except Exception as e:
        print(f'An error occurred: {e}')

    # # call weather
    # find_weather(city_choice, start_date, end_date)

    # call hotels
    find_hotels(city_choice, end_date, start_date)

    # # call activities
    final_results, results = get_activities(city_choice)
    if final_results:
        get_activity_details(final_results, results)

    # # call email
    # get_email()




# def find_weather(city, start_date, end_date): #JESS
#     pass
#
# def get_email(): #OLI
#     pass


def main(): # JOANA
    input_check = UserInputCheck()
    # Welcoming user and getting some basic details
    print("Hello! Welcome to Journey Genie! Let's start prepping your next holiday!")
    start_date = valid_date("First, please enter the start date for your holiday (DD-MM-YYYY): ")
    end_date = valid_date("Now, please enter the end date for your holiday (DD-MM-YYYY): ")

    knows_where = input_check.get_input("Do you know which country you'd like to go to? Y/N ")

    if knows_where == 'y':
        knows_destination(planner)
    elif knows_where == 'n':
        wants_random = input_check.get_input("No worries! We're here to help! Would you like us to make a random guess of a nice holiday place for you? Y/N ")
        if wants_random == 'y':
            take_me_anywhere(planner, start_date, end_date)
        elif wants_random == 'n':
            print("Ok! Let's tailor a holiday for you!")
            tailored_trip(planner)


if __name__ == "__main__":
    main()
    # pass
