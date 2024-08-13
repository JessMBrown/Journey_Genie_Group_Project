import requests
from pprint import pprint as pp

#api get request using required parameters
search_url = "https://engine.hotellook.com/api/v2/lookup.json"
location_search = input("Enter a city/country: ")
search_payload = {
    'query': location_search,
    'lang': 'en',
    'lookFor': 'both',
    'limit': 10,
    'convertCase': 1,
    'token': '4eb326f67e9461b5cd94edf6692193d3' #insert API token here
}
search_response = requests.get(search_url, params=search_payload)
#testing for successful response
if search_response.status_code == 200:
    print("request successful!")
else:
    print(f"Request failed with status code: {search_response.status_code}")

data = search_response.json()
#filtering to get city and country locations that match the search e.g return london not options like londonderry
#and allow users to select the right london e.g the london in england
matching_locations = [
    location for location in data['results']['locations']
    if location_search == location['cityName'].strip().lower() or location_search == location['countryName'].strip().lower()
]
if not matching_locations:
    print("No matching locations found.")
elif len(matching_locations) == 1:
    print("One match found:")
    selected_location = matching_locations[0]
    pp(selected_location)
else:
    print("Multiple matches found. Please select the correct one:")
    for i, location in enumerate(matching_locations, 1):
        print(f"{i}. {location['fullName']} (Hotels Count: {location['hotelsCount']})")

    choice = int(input("Enter the number corresponding to your choice: ")) - 1
    selected_location = matching_locations[choice]

    #variable that will be used in the hotel results api to seach for a hotel based on selected location
    hotel_locale = selected_location['id']