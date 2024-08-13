import requests

API_TOKEN = "4eb326f67e9461b5cd94edf6692193d3"


# Helper function to handle API response
def checking_api_response_success(response):
    if response.status_code == 200:
        return response.json()
    else:
        print(f"...request failed with status code: {response.status_code}")
        return None


# API call for the hotel or city search
def search_hotels_or_cities(query):
    url = "https://engine.hotellook.com/api/v2/lookup.json"
    search_payload = {
        'query': query,
        'lang': 'en',
        'lookFor': 'both',
        'limit': 10,
        'convertCase': 1,
        'token': API_TOKEN
    }

    response = requests.get(url, params=search_payload)
    print("...request successful" if response.status_code == 200 else "")
    return checking_api_response_success(response)


# API call for hotels within a city
def fetch_hotels_in_city(location_id, check_in, check_out, rooms, adults):
    url = "https://engine.hotellook.com/api/v2/cache.json"
    hotel_search_payload = {
        'locationId': location_id,
        'token': API_TOKEN,
        'limit': 10,
        'checkIn': check_in.strftime("%Y-%m-%d"),
        'checkOut': check_out.strftime("%Y-%m-%d"),
        'rooms': rooms,
        'adults': adults
    }

    response = requests.get(url, params=hotel_search_payload)
    return checking_api_response_success(response)


# API call for the price of hotels
def fetch_price(hotel_id=None, check_in=None, check_out=None, rooms=1, adults=2, currency='GBP'):
    price_url = "https://engine.hotellook.com/api/v2/cache.json"
    price_payload = {
        'checkIn': check_in.strftime("%Y-%m-%d"),
        'checkOut': check_out.strftime("%Y-%m-%d"),
        'currency': currency,
        'token': API_TOKEN,
        'limit': 1,
        'adults': adults,
        'rooms': rooms,
        'hotelId': hotel_id
    }

    response = requests.get(price_url, params=price_payload)
    return checking_api_response_success(response).get('priceAvg', None) if response.status_code == 200 else None


