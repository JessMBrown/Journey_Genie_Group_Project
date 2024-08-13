from Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque
from Config import activities_api_key, hotels_api_key, weather_api_key
from utils import UserInputCheck
import random


# def knows_destination():
#     chosen_country = input("Please, enter the name of the country: ")  # modify to make it a fixed list of countries
#     #  Make a list of cities to chose from
#     #  Call weather
#     #  call hotels function to get list of hotels
#     #  call activities function to make suggestions find_activities(city)
#     #  call email function
#
#
# def tailored_trip():
#     # take user input on what type of holiday he would like
#     # create code to get countries and get user to choose one
#     # call find cities to display list of cities
#     # call weather
#     # call hotels function to display hotels
#     # call activities function to display activities
#     # call email function to get email sent
#     pass
#
# def take_me_anywhere():
#     #  create code to random to call find country
#     random_countries = random.choices(country_list, k=5) # need to replace with name of list from db custom API
#
#     while True:
#         good_selection = input(f"Fancy any of these countries? {random_countries} Y/N ").lower().strip()
#         if good_selection == 'y':
#             country_choice = input('Please enter the name of the country: ')
#             break
#         elif good_selection == 'n':
#             continue
#         else:
#             print('Invalid answer! Please type Y or N ')
#
#     # call cities
#     city_choice = find_cities(country_choice)
#     # call weather
#     find_weather(city_choice)
#     # call hotels
#     find_hotels(city_choice)
#     # call activities
#     find_activities(city_choice)
#     # call email
#     get_email()
#     #(#  get favourites)

def find_cities(country): # or should it be find countries and cities?
    pass
def find_weather(city, start_date, end_date):
    pass
def find_hotels(city, num_adults, num_children):
    pass
def find_activities(city):
    input_check = UserInputCheck()
    opentripmap_api = OpenTripMapApi(activities_api_key)

    while True:
        try:
            coordinates = opentripmap_api.get_coordinates(city)
            if not coordinates:
                raise ValueError('Error! Coordinates are missing!')

            lat = coordinates['lat']
            lon = coordinates['lon']

            while True:
                # user input can take up to 3 separated by a comma but no space
                kinds_choices = ['historic', 'beaches', 'nature_reserves', 'theatres_and_entertainments',
                                 'museums', 'sport', 'amusements']
                kinds = input(
                    f'Please choose from the following list, which type of activity you would like ?(up to 3 choices) \n{kinds_choices} ')

                kinds = input_check.formatted_kinds_activities(kinds)  # calls method from utils to format the input
                kinds_list = kinds.split(',')
                if all(kind in kinds_choices for kind in kinds_list) and len(kinds_list) <= 3:
                    break
                else:
                    print('Invalid choices. Please check your spelling and/or enter 3 or fewer types! ')

            limit_per_kind = 5

            activities = opentripmap_api.get_activities(city, lat, lon, kinds)
            if not activities:
                print(f'Sorry, there are no {kinds_list} in {city}! ')
                continue

            # sort activities by rate
            sorted_activities = sorted(activities, key=lambda x: x.get('rate', 3), reverse=True)

            # splitting kinds
            split_kinds = kinds.split(',')

            # containers using deque for each kind of split_list
            kind_deques = {kind: deque(maxlen=limit_per_kind) for kind in split_kinds}

            # appending activities to each deque
            for activity in sorted_activities:
                activity_kind = activity['kinds']
                for kind in split_kinds:
                    if kind in activity_kind.split(','):
                        kind_deques[kind].append(activity)
                        break

            # joining deques together
            results = []
            for kind in split_kinds:
                results.extend(kind_deques[kind])

            final_results = [item['name'] for item in results]
            print(f'Here are the activities available to you in {city}:')
            pprint(final_results)

            while True:
                # to get activity details
                activity_choice = input(
                    'Do you want more details on any of them? If so type their name: ').lower().strip()  # or make a dropdown or a select or click on image/name
                final_results_lower = [name.lower() for name in final_results]
                if activity_choice not in final_results_lower:
                    print('This activity is not in the list of possible activities! ')
                    continue

                xid = None
                for item in results:
                    if activity_choice == item['name'].lower():
                        xid = item['xid']
                        break
                else:
                    print('Error. Activity not found.')
                    return

                details = opentripmap_api.get_activity_details(xid)
                if not details:
                    print("We were not able to retrieve the data for the selected activity! ")
                    return
                print(f'Here are the details for {activity_choice}:')
                pprint(details)

                break

            break

        except ValueError:
            print('Wrong input! ')
        except Exception:
            print('Error')

def get_email():
    pass
print(find_activities('London'))
# def save_chosen_suggestions():
#     pass
#
# def main():
#     input_check = UserInputCheck()
#     # Welcoming user and getting some basic details
#     print("Hello! Welcome to Journey Genie! Let's start prepping your next holiday!")
#     start_date = input("First, please enter the start date for your holiday (YYYY-MM-DD): ")
#     end_date = input("Now, please enter the end date for your holiday (YYYY-MM-DD): ")
#     num_adults = input('How many adults will you be? ')
#     num_children = input("How many children? ")
#     knows_where = input_check.get_input("Do you know which country you'd like to go to? Y/N ")
#
#     if knows_where == 'y':
#         knows_destination()
#     elif knows_where == 'n':
#         wants_random = input_check.get_input("No worries! We're here to help! Would you like us to make a random guess of a nice holiday place for you? Y/N ")
#         if wants_random == 'y':
#             take_me_anywhere()
#         elif wants_random == 'n':
#             print("Ok! Let's tailor a nice holiday for you!")
#             tailored_trip()


if __name__ == "__main__":
    # main()
    pass
