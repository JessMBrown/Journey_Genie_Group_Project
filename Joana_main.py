from Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque

"""
Little explanation before you dive in: I put fixed user choices and commented out user input possibilities 
(that i used for testing as I went)

"""
def knows_destination():
    chosen_country = input("Please, enter the name of the country: ")

def tailored_trip():
    pass

def take_me_anywhere():
    pass

####################### ACTIVITIES WITH OPENTRIPMAPS ####################################
def find_activities():  # literaly just wrote this to wrap it but haven't formated anything inside
    # Won't stay here. This is just a list of the different types of activities the APi would return.
    # To be used in dropdown or tick your choice display.
    kinds_choices = ['historic', 'beaches', 'nature_reserves', 'theatres_and_entertainments',
                     'museums', 'sport', 'amusements']

    city = 'London'
    # city = input('Which town would you like to go to ? ')  # replace by user input variable

    coordinates = opentripmap_api.get_coordinates(city)  # do not change
    if not coordinates:
        print('Error! Coordinates are missing!')
        exit()

    lat = coordinates['lat']  # do not change
    lon = coordinates['lon']  # do not change

    kinds = 'museums,sport,amusements'
    # kinds = input('Please choose which type of activity you would like ? ')
    # will need to be changed with user input can take up to 3 separated by a comma but no space

    limit_per_kind = 5  # do not change

    activities = opentripmap_api.get_activities(city, lat, lon, kinds)  # change 'city' with user input variable name
    # and 'kinds' by whatever type the user selected

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

    final_results = [(item['name'], item['rate']) for item in results]
    print(f'Here are the activities available to you in {city}:')  # change to what is necessary
    pprint(final_results)

    # to get activity details
    activity_choice = 'London Stadium'  # input('Do you want more details on any of them? If so type their name: ')

    xid = None
    for item in activities:
        if activity_choice == item['name']:
            xid = item['xid']
            break
    else:
        print('Error')
        return

    details = opentripmap_api.get_activity_details(xid)
    print(f'Here are the details for {activity_choice}:')
    pprint(details)

#######################################################################################

def get_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input in ['y', 'n']:
            return user_input
        print("Sorry, that's not a possible option. Please enter 'Y' or 'N'.")
def main():
    # probably put all api keys here and all calls to api files
    api_key = ''  # enter your own API
    opentripmap_api = OpenTripMapApi(api_key)  # do not change

    # Welcoming user and getting some basic details
    print("Hello! Welcome to Journey Genie! Let's start prepping your next holiday!")
    start_date = input("First, please enter the start date for your holiday (YYYY-MM-DD): ")
    end_date = input("Now, please enter the end date for your holiday (YYYY-MM-DD): ")
    num_adults = input('How many adults will you be?')
    num_children = input("How many children? ")
    knows_where = get_input("Do you know which country you'd like to go to? Y/N")

    if knows_where == 'y':
        knows_destination()
    elif knows_where == 'n':
        wants_random = get_input("No worries! We're here to help! Would you like us to make a random guess of a nice holiday place for you? Y/N")
        if wants_random == 'y':
            take_me_anywhere()
        elif wants_random == 'n':
            print("Ok! Let's tailor a nice holiday for you!")
            tailored_trip()



if __name__ == "__main__":
    main()
