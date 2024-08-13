from api import fetch_price, fetch_hotels_in_city, search_hotels_or_cities
from db_utils import valid_date

def main():
    begin_search = input("Enter a hotel or city: ")
    data = search_hotels_or_cities(begin_search)

    # ensuring that what the user searches matches up with a city name or hotel name
    matching_cities = [location for location in data['results']['locations'] if
                       location['cityName'].lower() == begin_search.lower()]

    matching_hotels = [hotel for hotel in data['results']['hotels'] if
                       begin_search.lower() in hotel['label'].lower()]

    combined_results = matching_cities + matching_hotels

    # allowing the user to select the correct search option
    if len(combined_results) > 1:
        print(f"We've found multiple options for '{begin_search}':")
        for index, option in enumerate(combined_results):
            print(f"{index + 1}. {option['fullName']}")

        choice = int(input("Enter the number of the desired option: "))
        if 1 <= choice <= len(combined_results):
            chosen_option = combined_results[choice - 1]
            print(f"You chose: {chosen_option['fullName']}")
        else:
            print("Invalid choice. Please run the script again and select a valid option.")
            return

    elif len(combined_results) == 1:
        chosen_option = combined_results[0]
        print(f"One option found: {chosen_option['fullName']}")

    else:
        print(f"No locations or hotels found matching the name '{begin_search}'.")
        return

    # getting the dates and number of rooms and adults
    check_in_date = valid_date("Enter check-in date (dd-mm-yyyy): ")
    check_out_date = valid_date("Enter check-out date (dd-mm-yyyy): ")

    while check_out_date <= check_in_date:
        print("Check-out date must be after the check-in date. Please enter the check-out date again.")
        check_out_date = valid_date("Enter check-out date (dd-mm-yyyy): ")

    adults = int(input("Enter the number of people: "))
    rooms = int(input("Enter the number of rooms you would like: "))

    # if a user selected a city
    if 'hotelsCount' in chosen_option:
        location_id = chosen_option['id']
        hotels = fetch_hotels_in_city(location_id, check_in_date, check_out_date, rooms, adults)
        if hotels:
            hotel_prices = []
            for hotel in hotels:
                price = fetch_price(hotel_id=hotel['hotelId'], check_in=check_in_date, check_out=check_out_date,
                                    rooms=rooms, adults=adults)
                hotel_prices.append({
                    'hotelName': hotel['hotelName'],
                    'hotelId': hotel['hotelId'],
                    'price': price
                })

            # sort by price asc order
            hotel_prices.sort(key=lambda x: x['price'])

            print(f"\nHotels in {chosen_option['fullName']} (sorted by price):")
            for index, hotel in enumerate(hotel_prices):
                print(f"{index + 1}. {hotel['hotelName']} - Total Price: {hotel['price']} GBP")

            hotel_choice = int(input("\nEnter the number corresponding to the hotel you would like to select: "))
            if 1 <= hotel_choice <= len(hotel_prices):
                chosen_hotel = hotel_prices[hotel_choice - 1]
                hotel_id = chosen_hotel['hotelId']
            else:
                print("Invalid choice. Please run the script again and select a valid option.")
                return
        else:
            print("No hotels found in this city.")
            return
    else:
        # if a user selected an exact hotel
        hotel_id = chosen_option['id']
        price = fetch_price(hotel_id=hotel_id, check_in=check_in_date, check_out=check_out_date, rooms=rooms,
                            adults=adults)
        if price is None:
            print(f"Price information is not available for hotel {chosen_option['fullName']}.")
        elif price == 0:
            print(f"Could not retrieve price for hotel {chosen_option['fullName']}.")
        else:
            print(f"Hotel: {chosen_option['fullName']} - Average Price: {price} GBP")

if __name__ == "__main__":
    main()
