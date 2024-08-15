from database.config_oli import HOST, PASSWORD, USER
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
                for city in cities:
                    print(city[0])
                while True:
                    city_choice = input("Which of the cities would you like to visit? ").strip().lower()
                    if city_choice in city_names:
                        return city_choice
                    else:
                        print(f"Invalid city name.")
            else:
                print(f"No cities found for {chosen_country}. Please try another country.")

        except DbConnectionError as e:
            print(f"Error fetching cities: {e}")

    def get_holiday_type_input(self):
        valid_holiday_types = ['history', 'beaches', 'museums', 'mountains', 'theatre',
                               'wine', 'fashion', 'modern', 'tourism', 'shopping']
        print(f"Valid holiday types to choose from: {', '.join(valid_holiday_types)}")
        while True:
            holiday_type = input("Enter the type of holiday you're interested in: ").strip().lower()
            if holiday_type in valid_holiday_types:
                return holiday_type
            else:
                print("Invalid holiday type. Please choose a valid option.")

    def get_holiday_type_cities(self):
        holiday_type = self.get_holiday_type_input()
        try:
            conditions = f"cities.keyword = '{holiday_type}'"
            columns = ['cities.city_name', 'countries.country_name']
            join = "INNER JOIN countries ON cities.country_code = countries.country_code"

            # Fetch all relevant cities
            cities = self.db.fetch_data(table_name="cities", columns=columns, join=join, conditions=conditions)

            if cities:
                # Limit results to 5 by slicing the list
                limited_cities = cities[:5]
                print(f"Cities for {holiday_type} holidays (showing up to 5 results):")
                for city in limited_cities:
                    print(f"{city[0]} in {city[1]}")
            else:
                print(f"No cities found for {holiday_type} holidays.")
        except DbConnectionError as e:
            print(f"Error fetching cities for {holiday_type} holidays: {e}")

    def get_holiday_type_countries(self):

        holiday_type = self.get_holiday_type_input()
        try:
            conditions = f"cities.keyword = '{holiday_type}'"
            columns = ['DISTINCT countries.country_name']
            join = "INNER JOIN cities ON countries.country_code = cities.country_code"

            # Fetch all relevant countries
            countries = self.db.fetch_data(table_name="countries", columns=columns, join=join, conditions=conditions)

            if countries:
                # Limit results to 5 by slicing the list
                limited_countries = countries[:5]
                print(f"Countries for {holiday_type} holidays (showing up to 5 results):")
                for country in limited_countries:
                    print(country[0])
            else:
                print(f"No countries found for {holiday_type} holidays.")
        except DbConnectionError as e:
            print(f"Error fetching countries for {holiday_type} holidays: {e}")

    def close(self):
        """Close the database connection."""
        self.db.close()
