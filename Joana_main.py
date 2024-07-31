from Joana_OpenTripMapAPI import OpenTripMapApi

#Won't stay here. This is just a list of the different types of activities the APi would return.
kinds_choices = ['interesting_places', 'historic', 'beaches', 'nature_reserves', 'cultural', 'theaters_and_entertainments', 'amusements', 'sport']

def main():
    api_key = 'ENTER API KEY HERE'
    opentripmap_api = OpenTripMapApi(api_key)

    city = 'Moscow'
    coordinates = opentripmap_api.get_coordinates(city)
    lat = coordinates['lat']
    lon = coordinates['lon']

    activities = opentripmap_api.get_activities(city, lat, lon, 'theaters_and_entertainments')
    print(activities)


if __name__ == "__main__":
    main()