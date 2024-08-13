import requests
from Config import activities_api_key

class OpenTripMapApi:
    def __init__(self, api_key):
        self.api_key = activities_api_key
        self.base_url = 'http://api.opentripmap.com/0.1/en'
# Need the coordinates of a place to run the get_activities method.

    def get_coordinates(self, city):
        endpoint = f"{self.base_url}/places/geoname"
        params = {
            'name': city,
            'apikey': self.api_key
        }
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException:
            print('Request failed')


# This method will return activities depending on the kinds the user will have selected can take up to 3 kinds.
    def get_activities(self, city, lat, lon, kinds, radius=80467, limit=50, rate=3):

        endpoint = f"{self.base_url}/places/autosuggest"
        params = {
            'name': city,
            'radius': radius,
            'lat': lat,
            'lon': lon,
            'kinds': kinds,
            'limit': limit,
            'rate': rate,
            'apikey': self.api_key
        }
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()

        # loop that goes through the different activities given by API but only their names.
            activities = []
            for features in response.json()['features']:
                activity_name = features['properties']['name']
                activity_kinds = features['properties']['kinds']
                activity_rate = features['properties']['rate']
                activity_xid = features['properties']['xid']
                activities.append({'name': activity_name, 'rate': activity_rate, 'kinds': activity_kinds, 'xid': activity_xid})
            return activities

        except requests.exceptions.RequestException:
            print('Request failed')


    def get_activity_details(self, xid):
        endpoint = f"{self.base_url}/places/xid/{xid}"

        params = {
            'xid': xid,
            'apikey': self.api_key
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException:
            print('Request failed')
