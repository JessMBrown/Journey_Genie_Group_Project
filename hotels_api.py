import requests
from hotels_config import API_TOKEN

# function to handle api response
def checking_api_response_success(response):
    if response.status_code == 200:
        return response.json()
    else:
        print(f"...request failed with status code: {response.status_code}")
        return None

# api call for the city search
def search_cities(query):
    url = "https://engine.hotellook.com/api/v2/lookup.json"
    search_payload = {
        'query': query,
        'lang': 'en',
        'lookFor': 'city',
        'limit': 10,
        'convertCase': 1,
        'token': API_TOKEN
    }

    # request to search for cities
    response = requests.get(url, params=search_payload)
    return checking_api_response_success(response)

# api call to fetch hotels with selected filters
def fetch_hotels_with_filters(location_id, check_in, check_out, selected_filters):
    url = "https://yasen.hotellook.com/tp/public/widget_location_dump.json"
    hotel_search_payload = {
        'id': location_id,
        'token': API_TOKEN,
        'check_in': check_in.strftime("%Y-%m-%d"),
        'check_out': check_out.strftime("%Y-%m-%d"),
        'currency': 'gbp',
        'language': 'en',
        'limit': 200
    }

    filtered_hotels = []
    for filter_type in selected_filters:
        hotel_search_payload['type'] = filter_type
        response = requests.get(url, params=hotel_search_payload)
        hotels = checking_api_response_success(response).get(filter_type, [])

        # add hotels to list only if they meet all filters
        if not filtered_hotels:
            filtered_hotels = hotels
        else:
            filtered_hotels = [hotel for hotel in filtered_hotels if hotel in hotels]

    return filtered_hotels

# api call for the price of hotels
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

    try:
        # request to get the price of the hotel
        response = requests.get(price_url, params=price_payload)
        if response.status_code == 200:
            response_json = checking_api_response_success(response)
            if response_json is not None:
                return response_json.get('priceAvg', "Price unavailable")
        return "Price unavailable"
    except Exception as e:
        print(f"Exception occurred while fetching price for hotel ID: {hotel_id}: {e}")
        return "Price unavailable"

# api call to get the hotel link
def fetch_hotel_details_with_links(location_id, check_in, check_out, adults=2, currency='GBP', language='en_us'):
    url = "https://engine.hotellook.com/api/v2/static/hotels.json"
    hotel_details_payload = {
        'locationId': location_id,
        'token': API_TOKEN,
    }

    response = requests.get(url, params=hotel_details_payload)
    hotels_data = checking_api_response_success(response)

    if hotels_data is None or 'hotels' not in hotels_data:
        return []

    hotels_with_links = []
    base_url = "https://search.hotellook.com/hotels"

    for hotel in hotels_data['hotels']:
        hotel_id = hotel['id']
        city_id = hotel['cityId']
        destination = hotel['name']['en'].replace(" ", "+")

        full_link = (
            f"{base_url}?=1&adults={adults}&checkIn={check_in.strftime('%Y-%m-%d')}"
            f"&checkOut={check_out.strftime('%Y-%m-%d')}&children=&cityId={city_id}"
            f"&currency={currency}&destination={destination}&hotelId={hotel_id}&language={language}&marker=support_travelpayouts.com"
        )

        hotels_with_links.append({
            'hotelName': hotel['name']['en'],
            'hotelId': hotel_id,
            'link': full_link
        })

    return hotels_with_links
