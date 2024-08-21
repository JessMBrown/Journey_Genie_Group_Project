from config import HOST, PASSWORD, USER
from database.db_utils_oli import Database, DbConnectionError


class Location:
    def __init__(self, host, user, password, db_name):
        """Initialize the database connection."""
        self.db = Database(host=host, user=user, password=password, db_name=db_name)

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
                print(f"Cities in {chosen_country}:")
                city_names = [city[0].lower() for city in cities]

                # Displaying cities with a number in front of them
                for index, city in enumerate(cities, start=1):
                    print(f"{index}. {city[0]}")

                while True:
                    try:
                        # Getting the user's choice by number
                        city_choice = int(input("Which of the cities would you like to visit? ").strip())
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

    # def get_holiday_type_cities(self):
    #     holiday_types = self.get_holiday_type_input()
    #
    #     try:
    #         conditions = f"cities.keyword IN ({', '.join(f'\'{ht}\'' for ht in holiday_types)})"
    #         columns = ['cities.city_name', 'countries.country_name', 'cities.keyword']
    #         join = "INNER JOIN countries ON cities.country_code = countries.country_code"
    #
    #         cities = self.db.fetch_data(table_name="cities", columns=columns, join=join, conditions=conditions)
    #
    #         if cities:
    #             limited_cities = cities[:5]
    #             print(f"Cities for {', '.join(holiday_types)} holidays (showing up to 5 results):")
    #             for index, city in enumerate(limited_cities, start=1):
    #                 print(f"{index}. {city[0]} in {city[1]} for {city[2]}")
    #         else:
    #             print(f"No cities found for {', '.join(holiday_types)} holidays.")
    #     except DbConnectionError as e:
    #         print(f"Error fetching cities for {', '.join(holiday_types)} holidays: {e}")

    # def get_holiday_type_countries(self):
    #     holiday_types = self.get_holiday_type_input()
    #
    #     try:
    #         conditions = f"cities.keyword IN ({', '.join(f'\'{ht}\'' for ht in holiday_types)})"
    #         columns = ['DISTINCT countries.country_name']
    #         join = "INNER JOIN cities ON countries.country_code = cities.country_code"
    #
    #         countries = self.db.fetch_data(table_name="countries", columns=columns, join=join, conditions=conditions)
    #
    #         if countries:
    #             limited_countries = countries[:5]
    #             print(f"Countries for {', '.join(holiday_types)} holidays (showing up to 5 results):")
    #             for index, country in enumerate(limited_countries, start=1):
    #                 print(f"{index}. {country[0]}")
    #         else:
    #             print(f"No countries found for {', '.join(holiday_types)} holidays.")
    #     except DbConnectionError as e:
    #         print(f"Error fetching countries for {', '.join(holiday_types)} holidays: {e}")

    def close(self):
        """Close the database connection."""
        self.db.close()