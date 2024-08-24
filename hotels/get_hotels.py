from hotels.hotels_api import fetch_price, fetch_hotels_with_filters, search_cities, fetch_hotel_details_with_links
from utils import UserInputCheck
import urllib.parse, emoji
from mail_and_favourites.get_favourites import SavingToFavourites
from config import HOST, PASSWORD, USER
from location.get_location import Location

class CityNotFoundError(Exception):
    pass

# creating instances for different class needed in this file
favourites_manager = SavingToFavourites()
input_check = UserInputCheck()
location_manager = Location(host=HOST, password=PASSWORD, user=USER, db_name='destinations')


# searching for a city to go to
def city_search(city_choice):
    while True:
        data = search_cities(city_choice)

        # loop to find a matching city
        for location in data['results']['locations']:
            if city_choice.lower() in location['cityName'].lower():
                return location

        raise CityNotFoundError(f"No locations found matching the name '{city_choice}'. Try again.")


def get_number_of_people():
    while True:
        try:
            adults = int(input("Enter the number of people (max 4 per booking): "))
            if adults > 4:
                print("The maximum number of people allowed within a single booking is 4. Please try again.")
            else:
                return adults
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# ensuring a valid number of rooms
def get_number_of_rooms(adults):
    while True:
        try:
            rooms = int(input("Enter the number of rooms (max 3): "))
            if rooms > 3:
                print("The maximum number of rooms allowed is 3. Please enter a valid number of rooms.")
            elif adults > rooms * 2:
                print("The number of people exceeds the 2-person capacity per room. Please enter more rooms.")
            else:
                return rooms
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_selected_filters():
    available_filters = [
        "center", "luxury", "3-stars", "4-stars", "5-stars",
        "business", "romantic", "family", "pets", "pool"
    ]
    print("\nAvailable Filters:")
    for index, filter_name in enumerate(available_filters, 1):
        print(f"{index}. {filter_name.capitalize()}")

    while True:
        selected_filters_input = input("\nEnter the numbers corresponding to the filters you'd like to apply (comma-separated): ")
        selected_filters_indexes = selected_filters_input.split(',')
        try:
            selected_filters = [available_filters[int(index) - 1] for index in selected_filters_indexes]
            if all(1 <= int(index) <= len(available_filters) for index in selected_filters_indexes):
                break
            else:
                print("Some selected filters are invalid. Please try again.")

        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers separated by a comma.")

    print('Loading...\U0000231B')
    return selected_filters


def find_hotels(location_id, start_date, end_date, selected_filters, rooms, adults):
    filtered_hotels = fetch_hotels_with_filters(location_id, start_date, end_date, selected_filters)
    hotel_prices = []

    for hotel in filtered_hotels:
        try:
            # getting the prices of all the hotels
            price = fetch_price(hotel_id=hotel['hotel_id'], check_in=start_date, check_out=end_date,
                                rooms=rooms, adults=adults)

            hotel_prices.append({
                'hotelName': hotel['name'],
                'hotelId': hotel['hotel_id'],
                'price': price if price is not None else "Price information unavailable"
            })

        except Exception as e:
            print(f"An error occurred while fetching price for hotel '{hotel['name']}': {e}")
            hotel_prices.append({
                'hotelName': hotel['name'],
                'hotelId': hotel['hotel_id'],
                'price': "Price information unavailable"
            })
    # sorting the price by asc order
    hotel_prices.sort(
        key=lambda x: x['price'] if isinstance(x['price'], (int, float)) else (
            float('inf') if x['price'] == "Price unavailable" else x['price'])
    )

    return hotel_prices

# link for the hotels
def display_hotels_with_links(hotel_prices, hotels_with_links, city_name, selected_filters):
    print(f"\nHotels in {city_name} with the filters: {(', '.join(selected_filters)).capitalize()} (by price asc):")


    for index, hotel in enumerate(hotel_prices):
        price_display = f"{hotel['price']} GBP" if isinstance(hotel['price'], (int, float)) else hotel['price']
        print(f"{index + 1}. {hotel['hotelName']} - Total Price: {price_display}")

        hotel_link = "Link not available"
        for h in hotels_with_links:
            if h['hotelId'] == hotel['hotelId']:
                hotel_link = h['link']

        # encoded so special characters can be read in the url
        hotel_link = urllib.parse.quote(hotel_link, safe=":/?&=")
        print(f"{hotel_link}")

# user can select a hotel from the options and choice is displayed
def get_hotel_choice(hotel_prices):
    while True:
        try:
            hotel_choice = int(input("\nEnter the number corresponding to the hotel you would like to select: "))
            if 1 <= hotel_choice <= len(hotel_prices):
                chosen_hotel = hotel_prices[hotel_choice - 1]
                print(f"\nYou selected: {chosen_hotel['hotelName']} - Total Price: {chosen_hotel['price']} GBP")
                return chosen_hotel
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# retrieve the country name for the chosen city
def get_cityID_for_city_in_country(city_choice, country_choice):
    try:
        city_id = location_manager.get_city_id(chosen_city=city_choice, chosen_country=country_choice)
        return str(city_id)
    except Exception as e:
        print(f'An error occurred: {e}')

def save_hotel_to_favourite(results, city_choice, city_id, country_choice, country_code):
    hotel_id, hotel_name = results['hotelId'], results['hotelName']

    # calling method from utils to check if user wants to save the activities
    favourites_manager.save_favourite_hotels(hotel_id, hotel_name, city_choice, city_id, input_check, country_choice, country_code)


def get_hotels(city_choice, start_date, end_date):
    while True:
        chosen_option = city_search(city_choice)
        adults = get_number_of_people()
        rooms = get_number_of_rooms(adults)
        selected_filters = get_selected_filters()
        country_choice, country_code = chosen_option['countryName'], chosen_option['countryCode'].lower()
        city_id = get_cityID_for_city_in_country(city_choice, country_choice)

        hotel_prices = find_hotels(chosen_option['id'], start_date, end_date, selected_filters, rooms, adults)

        if hotel_prices:
            hotels_with_links = fetch_hotel_details_with_links(chosen_option['id'], start_date, end_date, adults)
            display_hotels_with_links(hotel_prices, hotels_with_links, chosen_option['cityName'], selected_filters)
            while True:
                hotel_selected = get_hotel_choice(hotel_prices)
                if hotel_selected:
                    # call method from get_favourites to save favourites
                    save_hotel_to_favourite(hotel_selected, chosen_option['cityName'], city_id, country_choice, country_code)
                    # offering possibility to choose another hotel
                    other_details = input_check.get_input(f'\nWould you like to select another hotel? Y/N ')
                    if other_details != 'y':
                        saved_hotels = favourites_manager.get_favourites('hotels')
                        return saved_hotels
                else:
                    print('No hotel was selected. Please try again!')
        else:
            print("No hotels with valid prices were found. Please try another city or modify your criteria.")
            continue

    saved_hotels = favourites_manager.get_favourites('hotels')
    return saved_hotels

