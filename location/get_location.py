from db_utils_oli import Database, DbConnectionError
from utils import UserInputCheck

input_check = UserInputCheck()

class Location:
    def __init__(self, host, user, password, db_name):
        """Initialize the database connection."""
        self.db = Database(host=host, user=user, password=password, db_name=db_name)
        self.shown_cities = set()

    def get_countries(self):
        try:
            columns = ['country_name']
            table_name = 'countries'
            countries = self.db.fetch_data(table_name=table_name, columns=columns)
            country_list = [country[0] for country in countries]

            return country_list

        except DbConnectionError as e:
            print(f"Error fetching countries: {e}")

    def get_cities_by_country(self, chosen_country):
        try:
            conditions = f"countries.country_name = '{chosen_country}'"
            columns = ['cities.city_name']
            join = "INNER JOIN countries ON cities.country_code = countries.country_code"
            cities = self.db.fetch_data(table_name="cities", columns=columns, join=join, conditions=conditions)

            if cities:
                cities = [city for city in cities if city[0] not in self.shown_cities]
                if not cities:
                    print(f"All cities for {chosen_country} have been shown.")
                    return None

                print(f"\nCities in {chosen_country}:")
                city_names = [city[0].lower() for city in cities]

                # Displaying cities with a number in front of them
                for index, city in enumerate(cities, start=1):
                    print(f"{index}. {city[0]}")

                while True:
                    try:
                        # Getting the user's choice by number
                        city_choice = int(input("\nWhich of the cities would you like to visit? ").strip())
                        if 1 <= city_choice <= len(cities):
                            chosen_city = cities[city_choice - 1][0].lower()
                            return chosen_city
                        else:
                            print("Invalid choice. Please enter a number corresponding to one of the cities.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print(f"No cities found for {chosen_country}. Please try another country.")

        except DbConnectionError as e:
            print(f"Error fetching cities: {e}")

    def get_city_id(self, chosen_city, chosen_country):
        try:
            conditions = (f"cities.city_name = '{chosen_city}' AND "
                          f"countries.country_name = '{chosen_country}'")
            columns = ['cities.id']
            join = "INNER JOIN countries ON cities.country_code = countries.country_code"
            cities = self.db.fetch_data(table_name="cities", columns=columns, join=join, conditions=conditions)
            if cities:
                return cities[0][0]
            else:
                print('No matching city found.')

        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def get_holiday_type_input(self):
        valid_holiday_types = ['history', 'beaches', 'museums', 'mountains', 'theatre',
                               'wine', 'fashion', 'modern', 'tourism', 'shopping']
        print(f"Valid holiday types to choose from: {', '.join(valid_holiday_types)}")

        while True:
            holiday_types_input = input(
                "Enter the type(s) of holiday you're interested in (e.g., beaches, museums): ").strip().lower()
            holiday_types = [holiday.strip() for holiday in holiday_types_input.split(",")]

            if all(ht in valid_holiday_types for ht in holiday_types):
                return holiday_types
            else:
                print("Invalid holiday type(s). Please choose from the valid options.")

    def get_holiday_type_cities(self):
        holiday_types = self.get_holiday_type_input()

        # Resetting shown_cities for each new search
        self.shown_cities.clear()

        try:
            conditions = "cities.keyword IN ({})".format(', '.join("'{}'".format(ht) for ht in holiday_types))
            columns = ['cities.city_name', 'countries.country_name', 'cities.keyword']
            join = "INNER JOIN countries ON cities.country_code = countries.country_code"

            cities = self.db.fetch_data(table_name="cities", columns=columns, join=join, conditions=conditions)
            cities = [city for city in cities if city[0] not in self.shown_cities]

            if cities:
                limited_cities = cities[:5]
                print(f"\nCities for {', '.join(holiday_types)} holidays (showing up to 5 results):")
                for index, city in enumerate(limited_cities, start=1):
                    print(f"{index}. {city[0]} in {city[1]} for {city[2]}")

                # Adding the displayed cities to the shown_cities set
                self.shown_cities.update([city[0] for city in limited_cities])

                # Asking if any city interests the user
                is_interested = input_check.get_input("\nDoes any of these cities interest you? Y/N ")
                if is_interested == 'y':
                    while True:
                        try:
                            city_choice = int(
                                input("Please enter the number corresponding to the city you want to select: ").strip())
                            if 1 <= city_choice <= len(limited_cities):
                                chosen_city = limited_cities[city_choice - 1][0]
                                print(f"You have selected: {chosen_city}")
                                chosen_country = limited_cities
                                return chosen_city, chosen_country
                            else:
                                print("Invalid choice. Please enter a number corresponding to one of the cities.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                else:
                    print("No city selected.")
                    return None

            else:
                print(f"No cities found for {', '.join(holiday_types)} holidays.")
                return None

        except DbConnectionError as e:
            print(f"Error fetching cities for {', '.join(holiday_types)} holidays: {e}")
            return None

    def get_holiday_type_countries(self):
        holiday_types = self.get_holiday_type_input()

        try:
            conditions = f"cities.keyword IN ({', '.join(f'\'{ht}\'' for ht in holiday_types)})"
            columns = ['DISTINCT countries.country_name']
            join = "INNER JOIN cities ON countries.country_code = cities.country_code"

            countries = self.db.fetch_data(table_name="countries", columns=columns, join=join, conditions=conditions)

            if countries:
                limited_countries = countries[:5]
                print(f"Countries for {', '.join(holiday_types)} holidays (showing up to 5 results):")
                for index, country in enumerate(limited_countries, start=1):
                    print(f"{index}. {country[0]}")
            else:
                print(f"No countries found for {', '.join(holiday_types)} holidays.")
        except DbConnectionError as e:
            print(f"Error fetching countries for {', '.join(holiday_types)} holidays: {e}")

    def close(self):
        """Close the database connection."""
        self.db.close()