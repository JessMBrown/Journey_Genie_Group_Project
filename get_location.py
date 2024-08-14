from database.config_oli import HOST, PASSWORD, USER
from database.db_utils_oli import Database, DbConnectionError


class Location:
    def __init__(self, host, user, password, db_name):
        """Initialize the database connection."""
        self.db = Database(host=host, user=user, password=password, db_name=db_name)

    def get_cities_by_country(self, chosen_country):
        try:
            conditions = f"countries.country_name = '{chosen_country}'"
            columns = ['cities.city_name']
            join = "INNER JOIN countries ON cities.country_code = countries.country_code"
            cities = self.db.fetch_data(table_name="cities", columns=columns, join=join, conditions=conditions)

            if cities:
                print(f"Cities in {chosen_country}:")
                for city in cities:
                    print(city[0])
                print("Which of the cities would you like to visit?")
            else:
                print(f"No cities found for {chosen_country}")
                """
                print("Enter another country: ")
                planner.get_cities_by_country(chosen_country) <-- not this bc infinite loop
                looking for a way to come back to the beginning and repeat the process
                I thought we might do something like 
    
    while True:
        chosen_country = input("Enter a country name: ")
        if planner.get_cities_by_country(chosen_country):
            break  # Exit loop if cities were found
        else:
            # Optionally handle user retry logic or just loop again
            print("Please try another country.")
                
                But it would have to be added outside of the class/function so I guess I wanted to ask if 
                you're all fine with adding this? Or maybe it's already handled within your code. 
                """

        except DbConnectionError as e:
            print(f"Error fetching cities: {e}")

    def get_holiday_type_cities(self, holiday_type):
        valid_holiday_types = ['history', 'beaches', 'museums', 'mountains', 'theatre',
                               'wine', 'fashion', 'modern', 'tourism', 'shopping']

        """
        I'm also having issues with displaying the valid holiday types when asking about it as the question is outside
        of the function / class. Is it added later when used within the wider functions? Do we put the 
        valid_holiday_types twice to have it within the function for error handing and they for the user display when
        asking for input? 
        
        print(f"Valid holiday types to choose from: {', '.join(valid_holiday_types)}")
        """

        while holiday_type not in valid_holiday_types:
            print("Invalid holiday type. Please choose a valid option.")
            holiday_type = input(f"Enter a valid holiday type ({', '.join(valid_holiday_types)}): ").strip().lower()

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

    def get_holiday_type_countries(self, holiday_type):
        valid_holiday_types = ['history', 'beaches', 'museums', 'mountains', 'theatre',
                               'wine', 'fashion', 'modern', 'tourism', 'shopping']

        """
        I'm also having issues with displaying the valid holiday types when asking about it as the question is outside
        of the function / class. Is it added later when used within the wider functions? Do we put the 
        valid_holiday_types twice to have it within the function for error handing and they for the user display when
        asking for input? 

        print(f"Valid holiday types to choose from: {', '.join(valid_holiday_types)}")
        """

        while holiday_type not in valid_holiday_types:
            print("Invalid holiday type. Please choose a valid option.")
            holiday_type = input(f"Enter a valid holiday type ({', '.join(valid_holiday_types)}): ").strip().lower()

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


# Create an instance of the Location class
planner = Location(host=HOST, user=USER, password=PASSWORD, db_name='destinations')

# Example of fetching cities by country
chosen_country = input("Enter the country you want to visit: ").strip().capitalize()
planner.get_cities_by_country(chosen_country)

# Example of fetching cities by holiday type
# holiday_type = input("Enter the type of holiday you're interested in (e.g., beaches, museums): ").strip().lower()
# planner.get_holiday_type_cities(holiday_type)
#
# # Example of fetching countries by holiday type
# planner.get_holiday_type_countries(holiday_type)