import requests

"""
Will need to create a custom error.
"""

class OpenTripMapApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.opentripmap.com/0.1/en'
#Need the coordinates of a place to run the get_activities method.
    def get_coordinates(self, city):
        endpoint = f"{self.base_url}/places/geoname"
        params = {
            'name': city,
            'apikey': self.api_key
        }
        response = requests.get(endpoint, params=params)
        return response.json()
#this method will return activities depending on the kinds the user will have selected can take up to 3 kinds.
    def get_activities(self, city, lat, lon, kinds, radius=10000):
        endpoint = f"{self.base_url}/places/autosuggest"
        params = {
            'name': city,
            'radius': radius,
            'lat': lat,
            'lon': lon,
            'kinds': kinds,
            'apikey': self.api_key
        }
        response = requests.get(endpoint, params=params)
        return response.json()

# coordinates = OpenTripMapApi('API KEY')
# lat = coordinates.get_coordinates('Moscow')['lat']
# lon = coordinates.get_coordinates('Moscow')['lon']
# print(lat, lon)
# activities = OpenTripMapApi('API KEY')
# print(activities.get_activities('Moscow', lat, lon, kinds='Historical'))
