import requests
from pprint import pprint as pp
from travelPayoutsAPI_destination_search import hotel_locale

#api get request using required and optional parameters
hotels_url = "https://yasen.hotellook.com/tp/public/widget_location_dump.json"

params = {
    'check_in': '2024-09-01',
    'check_out': '2024-09-02',
    'currency': 'GBP',
    'language': 'en',
    'limit': 50,
    'type': 'popularity',
    'id': hotel_locale,
    'token': '**************************' #insert API token here
}

response = requests.get(hotels_url, params=params)
pp(f'Here are a list of hotels and their prices per night')
hotels_data = response.json()
#getting the hotel names and their prices, accounting for the fact that some hotels
# dont have the latest price information available from the API
for hotel in hotels_data['popularity']:
        hotel_name = hotel['name']
        last_price_info = hotel.get('last_price_info', None)
        if last_price_info is not None:
            hotel_price = last_price_info['price']
            print(f"Hotel Name: {hotel_name}, Price: {hotel_price} {params['currency']}")
        else:
            print(f"Hotel Name: {hotel_name}, Price information not available")