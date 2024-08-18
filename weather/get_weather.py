from pprint import pprint
from collections import deque

import requests.exceptions

import weather_api_search
from config import activities_api_key, hotels_api_key, weather_api_key
# from utils import UserInputCheck
import random
from datetime import datetime, timedelta


def knows_destination(start_date, end_date):  # KAREN
    chosen_country = input("Please, enter the name of the country: ")  # modify to make it a fixed list of countries
    #  Make a list of cities to chose from
    chosen_city = "London"
    #  Call weather
    find_weather(chosen_city, start_date, end_date)
    #  call hotels function to get list of hotels
    #  call activities function to make suggestions find_activities(city)
    #  call email function


# def tailored_trip(): # JOANA
#     # city/country function to display countries based on what he's looking for
#     country_choice = find_cities(preferences)
#     city_choice = find_cities(country_choice)
#     # call weather
#     find_weather(city_choice, start_date, end_date)
#     # call hotels
#     find_hotels(city_choice, start_date, end_date, num_adults, num_children)
#     # call activities
#     find_activities(city_choice)
#     # call email
#     get_email()
#     pass

# def take_me_anywhere(): # JOANA
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

# # call cities
# city_choice = find_cities(country_choice)
# # call weather
# find_weather(city_choice, start_date, end_date)
# # call hotels
# find_hotels(city_choice, start_date, end_date, num_adults, num_children)
# # call activities
# find_activities(city_choice)
# # call email
# get_email()
# #(#  get favourites)

# def find_cities(country): # or should it be find countries and cities? OLI
#     pass
def find_weather(chosen_city, start_date, end_date):
    endpoint_url = weather_api_endpoint_calculator(start_date)
    list_of_dates = create_list_of_dates(start_date, end_date)
    weather_for_dates = make_weather_api_request(chosen_city, start_date, end_date, endpoint_url, list_of_dates)
    get_minimum_maximum_average_temperature(chosen_city, weather_for_dates, endpoint_url)
    return weather_for_dates


def weather_api_endpoint_calculator(start_date):
    present_date = str(datetime.today().date())
    from_300_days_present_date = str(add_days(300))
    fourteen_days_in_the_future = str(add_days(14))
    fourteen_days_in_the_past = str(subtract_days(14))
    # if the start_date is +/- 14 days from present_date then cannot get weather due to api limitations
    if fourteen_days_in_the_past <= str(start_date) < present_date or fourteen_days_in_the_future > str(
            start_date) > present_date:
        print("Sorry, cannot fetch the weather for these dates")
        #     if the start_date is more than 300 days from present_date or is less than present_date
        #     then the endpoint_url = "history" - reasoning, the API only returns weather predictions
        #     300 days from todays date, so if the dates requested are more than the APIs limits for
        #     predictions use the data from the historic data
    elif str(start_date) > from_300_days_present_date or str(start_date) < present_date:
        endpoint_url = "history"
        return endpoint_url
    elif str(start_date) > present_date:
        endpoint_url = "future"
        return endpoint_url

    else:
        print("Cannot get weather for this date")


def add_days(number_of_days_to_add, today_date=datetime.today().date()):
    return today_date + timedelta(number_of_days_to_add)


def subtract_days(number_of_days_to_subtract, today_date=datetime.today().date()):
    return today_date - timedelta(number_of_days_to_subtract)


def create_list_of_dates(start_date, end_date):
    # convert start_date to a datetime.date format (YYYY-MM-DD)
    list_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    # convert end_date to a datetime.date format (YYYY-MM-DD)
    list_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    # create an empty list for the dates
    dates_list = []
    # set the starting value for the while loop
    current_date = list_start_date
    # while loop to iterate over each date between (and including) list_start_date and list_end_dates and append into
    # the list
    while current_date <= list_end_date:
        dates_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates_list


def make_weather_api_request(location, start_date, end_date, endpoint_url, list_of_dates):
    # separate the requests into two as the api contracts differ in payload and response
    # the endpoint for historic weather accepts a start_date and end_date and will give back everything needed
    if endpoint_url == "history":
        weather_for_dates = weather_api_search.GetWeatherByLocation(location, start_date,
                                                                    end_date).get_weather_by_location_and_date(
            endpoint_url)
        return weather_for_dates
    # the endpoint the for futures weather accepts one start date only and returns that info, so many requests
    # are needed for many dates of weather
    elif endpoint_url == "future":
        # create an empty list for all the dates needed to be requests
        weather_for_day = []
        # loop through list of individual dates to be searched for and append each response to list
        for item in list_of_dates:
            weather_for_dates = weather_api_search.GetWeatherByLocation(location, item,
                                                                        end_date).get_weather_by_location_and_date(
                endpoint_url)
            weather_for_day.append(weather_for_dates)
        # flatten the list so all list items can be searched
        flattened_list = []
        for sublist in weather_for_day:
            flattened_list.extend(sublist)
        return flattened_list
    else:
        print("Sorry, we are unable to retrieve the information for dates provided.")


def get_minimum_maximum_average_temperature(chosen_city, weather_for_dates, endpoint):
    # list with dates and temps
    # extract all temps
    average_temps = [weather_for_dates]
    print(weather_for_dates)
    find_min_val_from_dict(average_temps)
    find_max_val_from_dict(average_temps)
    string_list = {'average_temp': 14.5, 'date': '2024-10-01'}
    # {'average_temp': 14.5, 'date': '2024-10-01'}, {'average_temp': 14.5, 'date': '2024-10-01'}
    result = string_list.get("average_temp")
    print(result)

    # get the average for all dates
    avg_temp_for_dates = ''
    # get the minimum and maximum temps
    lowest_temp = ''
    highest_temp = ''

    if endpoint == "history":
        print(
            f"The weather last year on the same dates in {chosen_city} was an average of {avg_temp_for_dates} °C, with "
            f"the lowest being {lowest_temp} and the highest being {highest_temp}")
    else:
        print(
            f"The predicted weather for {chosen_city} on the selected will have an average of {avg_temp_for_dates} °C, with "
            f"the lowest being {lowest_temp} and the highest being {highest_temp}")


def find_min_val_from_dict(min_val_to_find):
    val = min_val_to_find
    # Using list comprehension and .get() method
    # Get values of particular key in list of dictionaries
    res = [min_val_to_find.get('average_temp', None) for min_val_to_find in val]
    print(res)


def find_max_val_from_dict(max_val_to_find):
    return max(max_val_to_find, key=max_val_to_find.get)


# def find_hotels(city, num_adults, num_children): NADIA
#     pass
# def find_activities(city):
#     input_check = UserInputCheck()
#     opentripmap_api = OpenTripMapApi(activities_api_key)

#     while True:
#         try:
#             coordinates = opentripmap_api.get_coordinates(city)
#             if not coordinates:
#                 raise ValueError('Error! Coordinates are missing!')
#
#             lat = coordinates['lat']
#             lon = coordinates['lon']
#
#             while True:
#                 # user input can take up to 3 separated by a comma but no space
#                 kinds_choices = ['historic', 'beaches', 'nature_reserves', 'theatres_and_entertainments',
#                                  'museums', 'sport', 'amusements']
#                 kinds = input(
#                     f'Please choose from the following list, which type of activity you would like ?(up to 3 choices) \n{kinds_choices} ')
#
#                 kinds = input_check.formatted_kinds_activities(kinds)  # calls method from utils to format the input
#                 kinds_list = kinds.split(',')
#                 if all(kind in kinds_choices for kind in kinds_list) and len(kinds_list) <= 3:
#                     break
#                 else:
#                     print('Invalid choices. Please check your spelling and/or enter 3 or fewer types! ')
#
#             limit_per_kind = 5
#
#             activities = opentripmap_api.get_activities(city, lat, lon, kinds)
#             if not activities:
#                 print(f'Sorry, there are no {kinds_list} in {city}! ')
#                 continue
#
#             # sort activities by rate
#             sorted_activities = sorted(activities, key=lambda x: x.get('rate', 3), reverse=True)
#
#             # splitting kinds
#             split_kinds = kinds.split(',')
#
#             # containers using deque for each kind of split_list
#             kind_deques = {kind: deque(maxlen=limit_per_kind) for kind in split_kinds}
#
#             # appending activities to each deque
#             for activity in sorted_activities:
#                 activity_kind = activity['kinds']
#                 for kind in split_kinds:
#                     if kind in activity_kind.split(','):
#                         kind_deques[kind].append(activity)
#                         break
#
#             # joining deques together
#             results = []
#             for kind in split_kinds:
#                 results.extend(kind_deques[kind])
#
#             final_results = [item['name'] for item in results]
#             print(f'Here are the activities available to you in {city}:')
#             pprint(final_results)
#
#             while True:
#                 # to get activity details
#                 activity_choice = input(
#                     'Do you want more details on any of them? If so type their name: ').lower().strip()  # or make a dropdown or a select or click on image/name
#                 final_results_lower = [name.lower() for name in final_results]
#                 if activity_choice not in final_results_lower:
#                     print('This activity is not in the list of possible activities! ')
#                     continue
#
#                 xid = None
#                 for item in results:
#                     if activity_choice == item['name'].lower():
#                         xid = item['xid']
#                         break
#                 else:
#                     print('Error. Activity not found.')
#                     return
#
#                 details = opentripmap_api.get_activity_details(xid)
#                 if not details:
#                     print("We were not able to retrieve the data for the selected activity! ")
#                     return
#                 print(f'Here are the details for {activity_choice}:')
#                 pprint(details)
#
#                 break
#
#             break
#
#         except ValueError:
#             print('Wrong input! ')
#         except Exception:
#             print('Error')
#
# def get_email(): #OLI
#     pass
# print(find_activities('London'))

def main():  # JOANA
    # input_check = UserInputCheck()
    # Welcoming user and getting some basic details
    print("Hello! Welcome to Journey Genie! Let's start prepping your next holiday!")
    start_date = input("First, please enter the start date for your holiday (YYYY-MM-DD): ")
    end_date = input("Now, please enter the end date for your holiday (YYYY-MM-DD): ")
    num_adults = input('How many adults will you be? ')
    num_children = input("How many children? ")
    # knows_where = input_check.get_input("Do you know which country you'd like to go to? Y/N ")
    knows_where = input("Do you know which country you'd like to go to? Y/N ")

    if knows_where == 'y':
        knows_destination(start_date, end_date)


# elif knows_where == 'n': wants_random = input_check.get_input("No worries! We're here to help! Would you like us to
# make a random guess of a nice holiday place for you? Y/N ") if wants_random == 'y': take_me_anywhere() elif
# wants_random == 'n': print("Ok! Let's tailor a holiday for you!") tailored_trip()
#
#
if __name__ == "__main__":
    main()
# pass
