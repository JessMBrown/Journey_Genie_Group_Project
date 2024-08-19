from hotels_api import fetch_price, fetch_hotels_with_filters, search_cities
from hotels_utils import get_valid_dates

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
        # search for the desired city
        chosen_option = city_search()

        # ensuring valid dates from utils file
        check_in_date, check_out_date = get_valid_dates()

        # handle number of people input
        adults_valid = False
        while not adults_valid:
            try:
                # number of people
                adults = int(input("Enter the number of people (max 4 per booking): "))
                if adults > 4:
                    print("The maximum number of people allowed within a single booking is 4. Please try again.")
                else:
                    adults_valid = True
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # handle number of rooms input
        rooms_valid = False
        while not rooms_valid:
            try:
                # number of rooms
                rooms = int(input("Enter the number of rooms (max 3): "))
                if rooms > 3:
                    print("The maximum number of rooms allowed is 3. Please enter a valid number of rooms.")
                elif adults > rooms * 2:
                    print("The number of people exceeds the 2-person capacity per room. Please enter more rooms.")
                else:
                    rooms_valid = True
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # getting the hotels in the desired city
        location_id = chosen_option['id']

        # show the filter options
        available_filters = [
            "center", "luxury", "3-stars", "4-stars", "5-stars",
            "business", "romantic", "family", "pets", "pool"
        ]
        print("\nAvailable Filters:")
        for index, filter_name in enumerate(available_filters, 1):
            print(f"{index}. {filter_name.capitalize()}")

        # getting the filters selected by the user
        selected_filters = input("Enter the numbers corresponding to the filters you'd like to apply (comma-separated): ")
        selected_filters = [available_filters[int(index) - 1] for index in selected_filters.split(",")]

        # fetching hotels based on location and filters
        filtered_hotels = fetch_hotels_with_filters(location_id, check_in_date, check_out_date, selected_filters)

        if filtered_hotels:
            city_selected = True
            hotel_prices = []
            for hotel in filtered_hotels:
                try:
                    # getting the prices of all the hotels
                    price = fetch_price(hotel_id=hotel['hotel_id'], check_in=check_in_date, check_out=check_out_date,
                                        rooms=rooms, adults=adults)
                    if price is not None:
                        # add hotel and price to list
                        hotel_prices.append({
                            'hotelName': hotel['name'],
                            'hotelId': hotel['hotel_id'],
                            'price': price
                        })
                    else:
                        hotel_prices.append({
                            'hotelName': hotel['name'],
                            'hotelId': hotel['hotel_id'],
                            'price': "Price information unavailable"
                        })
                except Exception as e:
                    print(f"An error occurred while fetching price for hotel '{hotel['name']}': {e}")
                    hotel_prices.append({
                        'hotelName': hotel['name'],
                        'hotelId': hotel['hotel_id'],
                        'price': "Price information unavailable"
                    })

            if hotel_prices:
                # sort hotels based on price and handling when the info is not available
                hotel_prices.sort(
                    key=lambda x: x['price'] if isinstance(x['price'], (int, float)) else (
                        float('inf') if x['price'] == "Price unavailable" else x['price'])
                )

                # display hotel and price info
                print(f"\nHotels in {chosen_option['cityName']} with the filters: {', '.join(selected_filters).capitalize()} (by price asc):")
                for index, hotel in enumerate(hotel_prices):
                    price_display = f"{hotel['price']} GBP" if isinstance(hotel['price'], (int, float)) else hotel['price']
                    print(f"{index + 1}. {hotel['hotelName']} - Total Price: {price_display}")

                hotel_selected = False
                while not hotel_selected:
                    try:
                        # ask user to select a hotel from the list
                        hotel_choice = int(input("\nEnter the number corresponding to the hotel you would like to select: "))
                        if 1 <= hotel_choice <= len(hotel_prices):
                            chosen_hotel = hotel_prices[hotel_choice - 1]
                            hotel_id = chosen_hotel['hotelId']
                            # display their selection
                            print(f"\nYou selected: {chosen_hotel['hotelName']} - Total Price: {price_display}")
                            hotel_selected = True
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                print("No hotels with valid prices were found. Please try another city or modify your criteria.")
                city_selected = False
        else:
            print("Unfortunately, no hotels were found for the selected criteria. Please try another city.")
            city_selected = False

if __name__ == "__main__":
    main()
