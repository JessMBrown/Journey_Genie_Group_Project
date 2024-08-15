from activities.Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque
from Config import activities_api_key
from utils import UserInputCheck


def get_activities(city):
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
