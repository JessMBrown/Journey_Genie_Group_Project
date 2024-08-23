from activities.Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque
from config import activities_api_key
from utils import UserInputCheck, SavingToFavourites
from hotels.get_hotels import city_search

# assigning classes from utils to variables
favourites_manager = SavingToFavourites()
input_check = UserInputCheck()

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

    final_results = process_and_display_activities(activities, city)
    get_activity_details(final_results, activities, city, country_choice)
    saved_activities = favourites_manager.get_favourites('activities')
    return saved_activities

# retrieve the country name for the chosen city
def get_country_for_city(city):
    # calling function in get hotels to retrieve the country name to be used in the save_favourites
    location_info = city_search(city)
    return location_info.get('countryName')

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
def get_activity_details(final_results, results, city_choice, country_choice):
    # calling API
    opentripmap_api = OpenTripMapApi(activities_api_key)

    while True:
        try:
            activity_choice = int(input("Please, enter the number corresponding to the activity you'd like more details on: "))
            # checking if user input is a possible number in the list of activities
            if 1 > activity_choice or activity_choice > len(final_results):
                print('Invalid number! Please try again ')
                continue

            # extracting name and id of the selected activity to use to call api and to display/save activity
            selected_activity = results[activity_choice - 1]
            display_activity_details(selected_activity, city_choice, country_choice)

        except ValueError:
            print('Please enter a valid number.')
            continue

        # offering possibility to get details on other activities
        other_details = input_check.get_input(f'Would you like details on another activity? Y/N ')
        if other_details != 'y':
            break

    return favourites_manager.get_favourites('activities')


def display_activity_details(selected_activity, city_choice, country_choice):
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

        # offering option to save activity
        favourites_manager.save_favourite_activities(selected_activity['xid'], selected_activity['name'], city_choice,
                                                     input_check, country_choice)



def extract_specific_details(details):
    # declaring what data from API we want to display
    return {
        'address': details.get('address', {}),
        'image': details.get('image', ''),
        'rate': details.get('rate', ''),
        'wikipedia': details.get('wikipedia', ''),
        'wikipedia_extracts': details.get('wikipedia_extracts', {}).get('html', '')
    }

def save_activity_to_favourite(results, city_choice, country_choice):
    for item in results:
        xid = item['xid']
        activity_name = item['name']
        # calling method from utils to check if user wants to save the activities
        favourites_manager.save_favourite_activities(xid, activity_name, city_choice, input_check, country_choice)


# find_and_display_activities('edinburgh')
# print(favourites_manager.get_favourites('activities'))
