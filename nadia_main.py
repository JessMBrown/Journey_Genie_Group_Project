from api import fetch_price, fetch_hotels_in_city, search_cities
from nadia_utils import get_valid_dates  # Updated import to use the new function

# searching for a city to go to
def city_search():
    while True:
        search = input("Enter a city: ")
        data = search_cities(search)

        # loop to find a matching city
        for location in data['results']['locations']:
            if search.lower() in location['cityName'].lower():
                city_full_name = f"{location['cityName']}, {location['countryName']}"
                print(city_full_name)
                return location  

        # if nothing is found, a prompt for the user to try again
        print(f"No locations found matching the name '{search}'. Try again.")


def main():
    city_selected = False
    while not city_selected:
        chosen_option = city_search()

        # ensuring valid dates from utils file
        check_in_date, check_out_date = get_valid_dates()

        adults_valid = False
        while not adults_valid:
            # number of people
            adults = int(input("Enter the number of people (max 4 per booking): "))
            if adults > 4:
                print("The maximum number of people allowed within a single booking is 4. Please try again.")
            else:
                adults_valid = True 

        rooms_valid = False
        while not rooms_valid:
            # number of rooms
            rooms = int(input("Enter the number of rooms (max 3): "))

            # within room capacity
            if rooms > 3:
                print("The maximum number of rooms allowed is 3. Please enter a valid number of rooms.")
            elif adults > rooms * 2:
                print("The number of people exceeds the 2-person capacity per room. Please enter more rooms.")
            else:
                rooms_valid = True

        # getting the hotels in the desired city
        location_id = chosen_option['id']
        hotels = fetch_hotels_in_city(location_id, check_in_date, check_out_date, rooms, adults)

        if hotels:
            city_selected = True  # flag to mark the city as valid if hotels are found
            hotel_prices = []
            for hotel in hotels:
                # getting the prices of all the hotels
                price = fetch_price(hotel_id=hotel['hotelId'], check_in=check_in_date, check_out=check_out_date,
                                    rooms=rooms, adults=adults)
                if price is not None:
                    # add hotel and price to list
                    hotel_prices.append({
                        'hotelName': hotel['hotelName'],
                        'hotelId': hotel['hotelId'],
                        'price': price
                    })

            # eliminate hotels with no price info and sort the list by price in ascending order
            hotel_prices = [hotel for hotel in hotel_prices if hotel['price'] is not None]
            hotel_prices.sort(key=lambda x: x['price'])

            # display hotel and price info
            print(f"\nHotels in {chosen_option['fullName']} (by price asc):")
            for index, hotel in enumerate(hotel_prices):
                print(f"{index + 1}. {hotel['hotelName']} - Total Price: {hotel['price']} GBP")

            hotel_selected = False
            while not hotel_selected:
                try:
                    # ask user to select a hotel from the list
                    hotel_choice = int(input("\nEnter the number corresponding to the hotel you would like to select: "))
                    if 1 <= hotel_choice <= len(hotel_prices):
                        chosen_hotel = hotel_prices[hotel_choice - 1]
                        hotel_id = chosen_hotel['hotelId']
                        # display their selection
                        print(f"\nYou selected: {chosen_hotel['hotelName']} - Total Price: {chosen_hotel['price']} GBP")
                        hotel_selected = True
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
        else:
            # if nothing is found, ask user to search for another city
            print("Unfortunately, no hotels were found for the selected criteria. Please try another city.")
            city_selected = False  # flag to reset the process to select a city


if __name__ == "__main__":
    main()
