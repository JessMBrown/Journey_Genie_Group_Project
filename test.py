import requests


def search_city_by_name(city_name, lang='en', limit=10, token='4eb326f67e9461b5cd94edf6692193d3'):
    url = "https://engine.hotellook.com/api/v2/lookup.json"

    # Parameters set to search specifically for cities by name
    params = {
        'query': city_name,  # The name of the city to search for
        'lang': lang,
        'lookFor': 'city',  # Specifically search for cities
        'limit': limit,
        'token': token
    }

    response = requests.get(url, params=params)

    # Check rate limit headers
    rate_limit_interval = response.headers.get('X-Ratelimit-Interval')
    rate_limit_remaining = response.headers.get('X-Ratelimit-Remaining')
    rate_limit_limit = response.headers.get('X-Ratelimit-Limit')

    if rate_limit_interval and rate_limit_remaining and rate_limit_limit:
        print(f"Rate Limit Interval: {rate_limit_interval} seconds")
        print(f"Rate Limit Remaining: {rate_limit_remaining} requests")
        print(f"Rate Limit: {rate_limit_limit} requests")
    else:
        print("Rate limit headers not found. You might not be rate limited.")

    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data.get('status')}")

        # Print out the entire JSON response for debugging
        print("\nFull JSON Response:")
        print(data)

        if 'results' in data:
            locations = data['results'].get('locations', [])

            if locations:
                print("\nCities Found:")
                for location in locations:
                    print(f"City Name: {location.get('cityName')}")
                    print(f"Full Name: {location.get('fullName')}")
                    print(f"Country Name: {location.get('countryName')}")
                    print(f"Country Code: {location.get('countryCode')}")
                    print(f"ID: {location.get('id')}")
                    print(f"Hotels Count: {location.get('hotelsCount')}")
                    print(
                        f"Coordinates: Latitude {location['location'].get('lat')}, Longitude {location['location'].get('lon')}")
                    print("-----")
            else:
                print("No city results found for the specified city name.")
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")


# Example usage with city name (e.g., "London")
search_city_by_name(city_name='new york', token='4eb326f67e9461b5cd94edf6692193d3')
