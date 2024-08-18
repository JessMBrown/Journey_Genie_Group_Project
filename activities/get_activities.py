from activities.Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque
from Config import activities_api_key
from utils import UserInputCheck, SavingToFavourites


favourites_manager = SavingToFavourites()
input_check = UserInputCheck()

def get_activities(city):
    opentripmap_api = OpenTripMapApi(activities_api_key)

    try:
        coordinates = opentripmap_api.get_coordinates(city)
        if not coordinates:
            raise ValueError('Error! Coordinates are missing!')

        lat = coordinates['lat']
        lon = coordinates['lon']

        while True:
            # user input can take up to 3 separated by a comma but no space
            kinds_choices = {
                'historic': 'historic',
                'beaches': 'beaches',
                'nature_reserves': 'nature reserves',
                'theatres_and_entertainments': 'theatres and entertainments',
                'museums': 'museums',
                'sport': 'sport',
                'amusements': 'amusements'
            }

            for index, display in enumerate(kinds_choices.values(), start=1):
                print(f'{index}. {display}')
            kinds = input(
                f'Please choose from this list, the number.s corresponding to the type of activity you would like ?'
                f'(up to 3 choices) ').strip().lower()

            kinds_indexes = input_check.formatted_kinds_activities(kinds)

            kinds_list = []
            for i in kinds_indexes:
                if i.isdigit():
                    index = int(i)
                    if 1 <= index <= len(kinds_choices):
                        kind_key = list(kinds_choices.keys())[index -1]
                        kinds_list.append(kind_key)

            if len(kinds_list) == 0 or len(kinds_list) > 3:
                print('Invalid choices. Please select up to 3 numbers in the list.')
                continue

            kinds = ','.join(kinds_list)

            activities = opentripmap_api.get_activities(city, lat, lon, kinds)
            if not activities:
                print(f'Sorry, there are no {kinds_list} in {city}! ')
                continue
            else:
                break

        limit_per_kind = 5

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

        for index, item in enumerate(final_results, start=1):
            print(f"{index}. {item}")

        return final_results, results

    except ValueError:
        print('Wrong input! ')

    except Exception as e:
        print(f'Unexpected error: {e}')

# to extract specific details
def extract_specific_details(details):
    extracted_details = {
        'address': details.get('address', {}),
        'image': details.get('image', ''),
        'rate': details.get('rate', ''),
        'wikipedia': details.get('wikipedia', ''),
        'wikipedia_extracts': details.get('wikipedia_extracts', {}).get('html', '')
    }
    return extracted_details
    # to get activity details
def get_activity_details(final_results, results):
    opentripmap_api = OpenTripMapApi(activities_api_key)

    try:
        wants_details = input_check.get_input('Do you want more details on any of them? Y/N ')
        if wants_details == 'n':
            for item in results:
                xid = item['xid']
                activity_name = item['name']
                favourites_manager.save_favourite_activities(xid, activity_name, input_check)
        elif wants_details == 'y':
            while True:
                try:
                    activity_choice = int(input('Enter the number corresponding to the activity: '))

                    if 1 > activity_choice or activity_choice > len(final_results):
                        print('Invalid number! Please try again ')
                        continue

                    selected_activity = results[activity_choice -1]
                    xid = selected_activity['xid']
                    activity_name = selected_activity['name']

                    details = opentripmap_api.get_activity_details(xid)
                    if not details:
                        print("We were not able to retrieve the data for the selected activity! ")
                        continue

                    activity_details = extract_specific_details(details)
                    print(f'Here are the details for {activity_name}:')
                    pprint(activity_details)

                    favourites_manager.save_favourite_activities(xid, activity_name, input_check)

                    other_details = input_check.get_input(f'Would you like details on another activity? Y/N ')
                    if other_details != 'y':
                        print('OK! Email stuff now')
                        break
                    else:
                        continue

                except ValueError:
                    print('Please enter a valid number.')

            return favourites_manager.get_favourites('activities')

    except ValueError:
        print('Wrong input! ')
    except Exception as e:
        print(f'Unexpected error: {e}')


# final_results, results = get_activities('edinburgh')
# if final_results:
#     print(get_activity_details(final_results, results))