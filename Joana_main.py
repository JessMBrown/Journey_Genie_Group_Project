from Joana_OpenTripMapAPI import OpenTripMapApi

"""
Need fixing : 3 choices max in kinds
Can make a new method to get details on the activities. And possibly pictures or something.
"""

# Won't stay here. This is just a list of the different types of activities the APi would return.
# To be used in dropdown or tick your choice display.
kinds_choices = ['interesting_places', 'historic', 'beaches',
                 'nature_reserves', 'theatres_and_entertainments', 'museums', 'sport', 'amusements']


def main():
    api_key = ''  # enter your own API
    opentripmap_api = OpenTripMapApi(api_key)  # do not change

    city = 'London'  # replace by user input variable
    coordinates = opentripmap_api.get_coordinates(city)  # do not change
    lat = coordinates['lat']  # do not change
    lon = coordinates['lon']  # do not change
    rates = '3'  # rate is maximum 3(but for some reason some activities have a rate of 7...
    # but if you enter 7 as a rate option, it throws an error)
    # rates need to be changed with user input. Can take several choices.
    kinds = 'amusements', 'sport'  # will need to be changed with user input can take up to 3.

    activities = opentripmap_api.get_activities(city, lat, lon, kinds, rates)  # change 'city' with user input name
    # and 'kinds' by whatever type the user selected
    print(activities)  # probably replace by a return and use it in some text to be displayed


if __name__ == "__main__":
    main()
