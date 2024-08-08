import requests
from config import weatherApiKey

base_url = "https://api.weatherapi.com/v1"
history_endpoint = "history.json"
future_endpoint = "future.json?q=London&dt=2024-08-22&key="
weatherapi_key = weatherApiKey


class GetWeatherByLocation:
    pass


# Need the location name, the start date and end date of the date ranges to be searched
def get_weather_by_location_and_date(location, start_date, end_date):
    endpoint = f"{base_url}/{history_endpoint}"
    params = {
        'q': location,
        'dt': start_date,
        'end_dt': end_date,
        'key': weatherapi_key
    }
    try:
        weather_response = requests.get(endpoint, params=params)
        weather_response.raise_for_status()
        # flatten the results of the days weather
        forecast_for_dates = weather_response.json()['forecast']['forecastday']
        print(forecast_for_dates)
        # Create a list and loop through each date and extract the average temp (avgtemp_c) for that day in Celsius
        # and add to the list
        average_temp_for_dates_list = []
        for weather_data in forecast_for_dates:
            days_date = weather_data['date']
            days_average_temp_in_c = weather_data['day']['avgtemp_c']
            average_temp_for_dates_list.append({'date': days_date, 'average_temp': days_average_temp_in_c})
            print(days_date)
            print(days_average_temp_in_c)
        print(average_temp_for_dates_list)
        return average_temp_for_dates_list

    except requests.exceptions.RequestException:
        print('Request failed')


location = "London"
start_date = "2023-12-31"
end_date = "2024-01-05"
get_weather_by_location_and_date(location, start_date, end_date)
