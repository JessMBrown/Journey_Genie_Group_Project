# import requests
# from Config import weather_api_key
#
#
# class GetWeatherByLocation:
#
#     # Need the location name, the start date and end date of the date ranges to be searched
#     # base url and api key are both static so not passed in
#
#     def __init__(self, location, start_date, end_date):
#         self.location = location
#         self.start_date = start_date
#         self.end_date = end_date
#         self.base_url = "https://api.weatherapi.com/v1"
#         self.api_key = weather_api_key
#
#     def get_weather_by_location_and_date(self, date_url="history"):
#         # full url is from the base + desired endpoint
#         url = date_url
#         endpoint = f"{self.base_url}/{url}.json"
#         params = {
#             'q': self.location,
#             'dt': self.start_date,
#             'end_dt': self.end_date,
#             'key': self.api_key
#         }
#         # create an empty list for any valid responses to be stored in
#         average_temp_for_dates_list = []
#         # a try catch loop for iterating over anything that is returned from a successful request
#         try:
#             weather_response = requests.get(endpoint, params=params)
#             weather_response.raise_for_status()
#             # flatten the results of the days weather
#             forecast_for_dates = weather_response.json()['forecast']['forecastday']
#             # Create a list and loop through each date and extract the average temp (avgtemp_c) for that day in Celsius
#             # and add to the list
#             for weather_data in forecast_for_dates:
#                 days_date = weather_data['date']
#                 days_average_temp_in_c = weather_data['day']['avgtemp_c']
#                 average_temp_for_dates_list.append({'date': days_date, 'average_temp': days_average_temp_in_c})
#             return average_temp_for_dates_list
#
#         except requests.exceptions.HTTPError as httpError:
#             print("Http Error: ", httpError)
#         except requests.exceptions.ConnectionError as connectionError:
#             print("Error Connecting: ", connectionError)
#         except requests.exceptions.Timeout as timedOutError:
#             print("Timeout Error: ", timedOutError)
#         except requests.exceptions.RequestException as err:
#             print("Request failed due to ", err)