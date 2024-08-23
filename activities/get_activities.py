from activities.Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque
from config import activities_api_key
from location.get_location import Location
from utils import UserInputCheck
from mail_and_favourites.get_favourites import SavingToFavourites
from hotels.get_hotels import city_search
from config import HOST, PASSWORD, USER

# assigning classes from utils to variables
favourites_manager = SavingToFavourites()
input_check = UserInputCheck()
location_manager = Location(host=HOST, user=USER, password=PASSWORD, db_name='destinations')

<<<<<<< HEAD

def get_activities(city):
    # calling API
    opentripmap_api = OpenTripMapApi(activities_api_key)

    # API parameters requires latitude and longitude so need to find those thanks to API
    try:
        coordinates = opentripmap_api.get_coordinates(city)
        if not coordinates:
            raise ValueError('Error! Coordinates are missing!')

        lat = coordinates['lat']
        lon = coordinates['lon']

        # Starting a loop to continue prompting user if needed
        while True:
            # creating dictionary to be able to have a displayable name and the name in a format the API requires
            kinds_choices = {
                'historic': 'historic',
                'beaches': 'beaches',
                'nature_reserves': 'nature reserves',
                'theatres_and_entertainments': 'theatres and entertainments',
                'museums': 'museums',
                'sport': 'sport',
                'amusements': 'amusements'
            }

            # assigning numbers in front of each value to handle user input better
            for index, display in enumerate(kinds_choices.values(), start=1):
                print(f'{index}. {display}')
            # getting user input
            kinds = input(
                f'Please choose from this list, the number.s corresponding to the type of activity you would like ?'
                f'(up to 3 choices) ').strip().lower()

            # running input through method in utils to check format
            kinds_indexes = input_check.formatted_kinds_activities(kinds)

            # creating a list of input data and turning it back from numbers to words
            kinds_list = []
            for i in kinds_indexes:
                if i.isdigit():
                    index = int(i)
                    if 1 <= index <= len(kinds_choices):
                        kind_key = list(kinds_choices.keys())[index - 1]
                        kinds_list.append(kind_key)

            # checking user did not enter more than 3 options
            if len(kinds_list) == 0 or len(kinds_list) > 3:
                print('Invalid choices. Please select up to 3 numbers in the list.')
=======
# main function
def find_and_display_activities(city):
    country_choice = get_country_for_city(city)
    coordinates = get_city_coordinates(city)
    if not coordinates:
        return

    kinds = get_user_selected_kinds()
    if not kinds:
        return

    activities = fetch_activities(city, coordinates, kinds)
    if not activities:
        return

    city_id = get_cityID_for_city_in_country(city, country_choice)
    country_code = extract_country_code_from_activities(activities)
    final_results = process_and_display_activities(activities, city)

    get_activity_details(final_results, activities, city, city_id, country_choice, country_code)
    saved_activities = favourites_manager.get_favourites('activities')
    return saved_activities

# retrieve the country name for the chosen city
def get_country_for_city(city):
    # calling function in get hotels to retrieve the country name to be used in the save_favourites
    location_info = city_search(city)
    return location_info.get('countryName')

# retrieve the country name for the chosen city
def get_cityID_for_city_in_country(city_choice, chosen_country):
    try:
        city_id = location_manager.get_city_id(chosen_city=city_choice, chosen_country=chosen_country)
        return str(city_id)

    except Exception as e:
        print(f'An error occurred: {e}')

def get_city_coordinates(city):
    # calling API
    opentripmap_api = OpenTripMapApi(activities_api_key)
    coordinates = opentripmap_api.get_coordinates(city)
    if not coordinates:
        raise ValueError('Error! Coordinates are missing!')
    return coordinates


def get_user_selected_kinds():
    # creating dictionary to be able to have a displayable name and the name in a format the API requires
    kinds_choices = {
        'historic': 'historic',
        'beaches': 'beaches',
        'nature_reserves': 'nature reserves',
        'theatres_and_entertainments': 'theatres and entertainments',
        'museums': 'museums',
        'sport': 'sport',
        'amusements': 'amusements'
    }

    # assigning numbers in front of each value to handle user input better
    for index, display in enumerate(kinds_choices.values(), start=1):
        print(f'{index}. {display}')
    # getting user input
    kinds = input(
        f'Please choose from this list, the number.s corresponding to the type of activity you would like ?'
        f'(up to 3 choices) ').strip().lower()

    # running input through method in utils to check format
    kinds_indexes = input_check.formatted_kinds_activities(kinds)

    # creating a list of input data and turning it back from numbers to words
    kinds_list = []
    for i in kinds_indexes:
        if i.isdigit():
            index = int(i)
            if 1 <= index <= len(kinds_choices):
                kind_key = list(kinds_choices.keys())[index -1]
                kinds_list.append(kind_key)

    # checking user did not enter more than 3 options
    if len(kinds_list) == 0 or len(kinds_list) > 3:
        print('Invalid choices. Please select up to 3 numbers in the list.')
        return None

    # making sure words a separated by commas while returning them
    return ','.join(kinds_list)

def fetch_activities(city, coordinates, kinds):
    # calling API function to get data and throwing error if no data
    opentripmap_api = OpenTripMapApi(activities_api_key)
    lat, lon = coordinates['lat'], coordinates['lon']
    activities = opentripmap_api.get_activities(city, lat, lon, kinds)

    if not activities:
        print(f'Sorry, there are no {kinds} in {city}! ')

    return activities

# function to extract the country_code
def extract_country_code_from_activities(activities):
    if activities:
        address = activities[0].get('address', {})
        return address.get('country_code', 'Unknown')
    return 'Unknown'


def process_and_display_activities(activities, city):
    # allowing 5 possibilities per type of activity as some have thousands
    limit_per_kind = 5
    kinds = ','.join(set(kind for activity in activities for kind in activity['kinds'].split(',')))
    # splitting kinds
    split_kinds = kinds.split(',')
    # containers using deque for each kind of split_list
    kind_deques = {kind: deque(maxlen=limit_per_kind) for kind in split_kinds}
    # sort activities by rate
    sorted_activities = sorted(activities, key=lambda x: x.get('rate', 3), reverse=True)

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

    # creating a list of activities and adding a number in front
    final_results = [item['name'] for item in results]
    print(f'Here are the activities available to you in {city}:')

    for index, item in enumerate(final_results, start=1):
        print(f"{index}. {item}")

    return final_results

# to extract specific details
def get_activity_details(final_results, results, city_choice, city_id, country_choice, country_code):
    # calling API
    opentripmap_api = OpenTripMapApi(activities_api_key)

    while True:
        try:
            activity_choice = int(input("Please, enter the number corresponding to the activity you'd like more details on: "))
            # checking if user input is a possible number in the list of activities
            if 1 > activity_choice or activity_choice > len(final_results):
                print('Invalid number! Please try again ')
>>>>>>> joana_branch
                continue

            # extracting name and id of the selected activity to use to call api and to display/save activity
            selected_activity = results[activity_choice - 1]
            display_activity_details(selected_activity, city_choice, city_id, country_choice)

        except ValueError:
            print('Please enter a valid number.')
            continue

        # offering possibility to get details on other activities
        other_details = input_check.get_input(f'Would you like details on another activity? Y/N ')
        if other_details != 'y':
            break

    return favourites_manager.get_favourites('activities')


def display_activity_details(selected_activity, city_choice, city_id, country_choice):
        # calling API function
        opentripmap_api = OpenTripMapApi(activities_api_key)
        details = opentripmap_api.get_activity_details(selected_activity['xid'])

        # if error loops back to offer to select another activity
        if not details:
            print("We were not able to retrieve the data for the selected activity! ")
            return

        # calling function above to retrieve format for data to be displayed and displaying it
        activity_details = extract_specific_details(details)
        print(f'Here are the details for {selected_activity['name']}:')
        pprint(activity_details)

        #extracting country_code from details to use in save_favourite
        address = details.get('address', {})
        country_code = address.get('country_code', 'Unknown')
        # offering option to save activity
        favourites_manager.save_favourite_activities(selected_activity['xid'], selected_activity['name'], city_choice, city_id,
                                                     input_check, country_choice, country_code)

        return details

<<<<<<< HEAD
    except ValueError:
        print('Wrong input! ')

    except Exception as e:
        print(f'Unexpected error: {e}')


# to extract specific details
=======
>>>>>>> joana_branch
def extract_specific_details(details):
    # declaring what data from API we want to display
    return {
        'address': details.get('address', {}),
        'image': details.get('image', ''),
        'rate': details.get('rate', ''),
        'wikipedia': details.get('wikipedia', ''),
        'wikipedia_extracts': details.get('wikipedia_extracts', {}).get('html', '')
    }

def save_activity_to_favourite(results, city_choice, country_choice, city_id, country_code):
    for item in results:
        xid = item['xid']
        activity_name = item['name']
        # calling method from utils to check if user wants to save the activities
        favourites_manager.save_favourite_activities(xid, activity_name, city_choice, city_id, input_check, country_choice, country_code)


<<<<<<< HEAD
def get_activity_details(final_results, results, city_choice):
    # calling API
    opentripmap_api = OpenTripMapApi(activities_api_key)
    chosen_country = state.chosen_country

    try:
        # offering possibility to get details on each activity
        wants_details = input_check.get_input('Do you want more details on any of them? Y/N ')
        if wants_details == 'n':
            for item in results:
                xid = item['xid']
                activity_name = item['name']
                # calling method from utils to check if user wants to save the activities
                favourites_manager.save_favourite_activities(xid, activity_name, city_choice, input_check,
                                                             chosen_country)
        elif wants_details == 'y':
            while True:
                try:
                    activity_choice = int(input('Enter the number corresponding to the activity: '))

                    # checking if user input is a possible number in the list of activities
                    if 1 > activity_choice or activity_choice > len(final_results):
                        print('Invalid number! Please try again ')
                        continue

                    # extracting name and id of the selected activity to use to call api and to display/save activity
                    selected_activity = results[activity_choice - 1]
                    xid = selected_activity['xid']
                    activity_name = selected_activity['name']

                    # calling API function
                    details = opentripmap_api.get_activity_details(xid)
                    # if error loops back to offer to select another activity
                    if not details:
                        print("We were not able to retrieve the data for the selected activity! ")
                        continue

                    # calling function above to retrieve format for data to be displayed and displaying it
                    activity_details = extract_specific_details(details)
                    print(f'Here are the details for {activity_name}:')
                    pprint(activity_details)

                    # offering option to save activity
                    favourites_manager.save_favourite_activities(xid, activity_name, city_choice, input_check,
                                                                 chosen_country)

                    # offering possibility to get details on other activities
                    other_details = input_check.get_input(f'Would you like details on another activity? Y/N ')
                    if other_details != 'y':
                        break

                except ValueError:
                    print('Please enter a valid number.')
            # returning favourite list to use to save to db
            return favourites_manager.get_favourites('activities')

    except ValueError:
        print('Wrong input! ')
    except Exception as e:
        print(f'Unexpected error: {e}')

# final_results, results = get_activities('edinburgh')
# if final_results:
#     print(get_activity_details(final_results, results, 'edinburgh'))
=======
# find_and_display_activities('edinburgh')
# print(favourites_manager.get_favourites('activities'))
>>>>>>> joana_branch
