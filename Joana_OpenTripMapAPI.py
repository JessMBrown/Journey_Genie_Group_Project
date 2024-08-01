import requests

"""
Will need to create error handling with try except...
"""


class OpenTripMapApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.opentripmap.com/0.1/en'
# Need the coordinates of a place to run the get_activities method.

    def get_coordinates(self, city):
        endpoint = f"{self.base_url}/places/geoname"
        params = {
            'name': city,
            'apikey': self.api_key
        }
        response = requests.get(endpoint, params=params)
        return response.json()

# This method will return activities depending on the kinds the user will have selected can take up to 3 kinds.
    def get_activities(self, city, lat, lon, kinds, rates, radius=1000000):
        str_rates = ','.join(map(str, rates))

        endpoint = f"{self.base_url}/places/autosuggest"
        params = {
            'name': city,
            'radius': radius,
            'lat': lat,
            'lon': lon,
            'kinds': kinds,
            'rate': str_rates,
            'apikey': self.api_key
        }
        response = requests.get(endpoint, params=params)

        # loop that goes through the different activities given by API but only their names.
        activities = []
        for features in response.json()['features']:
            activity_name = features['properties']['name']
            activity_rate = features['properties']['rate']
            activities.append({'name': activity_name, 'rate': activity_rate})
        return activities
