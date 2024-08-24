from weather.weather_api_search import GetWeatherByLocation
from datetime import datetime, timedelta
import emoji

get_weather = GetWeatherByLocation(location=None, start_date=None, end_date=None)


def find_weather(chosen_city, start_date, end_date):
    endpoint_url = weather_api_endpoint_calculator(start_date)
    list_of_dates = create_list_of_dates(start_date, end_date)
    weather_for_dates = make_weather_api_request(chosen_city, start_date, end_date, endpoint_url, list_of_dates)
    get_minimum_maximum_average_temperature(chosen_city, weather_for_dates, endpoint_url)
    return weather_for_dates


def weather_api_endpoint_calculator(start_date):
    present_date = str(datetime.today().date())
    from_300_days_present_date = str(add_days(300))
    fourteen_days_in_the_future = str(add_days(14))
    fourteen_days_in_the_past = str(subtract_days(14))
    # if the start_date is +/- 14 days from present_date then cannot get weather due to api limitations
    if fourteen_days_in_the_past <= str(start_date) < present_date or fourteen_days_in_the_future > str(
            start_date) > present_date:
        print("Sorry, cannot fetch the weather for these dates")
        #     if the start_date is more than 300 days from present_date or is less than present_date
        #     then the endpoint_url = "history" - reasoning, the API only returns weather predictions
        #     300 days from today's date, so if the dates requested are more than the APIs limits for
        #     predictions use the data from the historic data
    elif str(start_date) > from_300_days_present_date or str(start_date) < present_date:
        endpoint_url = "history"
        return endpoint_url
    elif str(start_date) > present_date:
        endpoint_url = "future"
        return endpoint_url

    else:
        print("Cannot get weather for this date")


def add_days(number_of_days_to_add, today_date=datetime.today().date()):
    return today_date + timedelta(number_of_days_to_add)


def subtract_days(number_of_days_to_subtract, today_date=datetime.today().date()):
    return today_date - timedelta(number_of_days_to_subtract)


def create_list_of_dates(start_date, end_date):
    # convert start_date to a datetime.date format (YYYY-MM-DD)
    # list_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    # convert end_date to a datetime.date format (YYYY-MM-DD)
    # list_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    # create an empty list for the dates
    dates_list = []
    # set the starting value for the while loop
    current_date = start_date
    # while loop to iterate over each date between (and including) list_start_date and list_end_dates and append into
    # the list
    while current_date <= end_date:
        dates_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates_list


def make_weather_api_request(location, start_date, end_date, endpoint_url, list_of_dates):
    # separate the requests into two as the api contracts differ in payload and response
    # the endpoint for historic weather accepts a start_date and end_date and will give back everything needed
    if endpoint_url == "history":
        weather_for_dates = (GetWeatherByLocation(location, start_date, end_date).get_weather_by_location_and_date
                             (endpoint_url))
        return weather_for_dates
    # the endpoint the for futures weather accepts one start date only and returns that info, so many requests
    # are needed for many dates of weather
    elif endpoint_url == "future":
        # create an empty list for all the dates needed to be requests
        weather_for_day = []
        # loop through list of individual dates to be searched for and append each response to list
        for item in list_of_dates:
            weather_for_dates = GetWeatherByLocation(location, item, end_date).get_weather_by_location_and_date(
                endpoint_url)
            weather_for_day.append(weather_for_dates)
        # flatten the list so all list items can be searched
        flattened_list = []
        for sublist in weather_for_day:
            flattened_list.extend(sublist)
        return flattened_list
    else:
        print("Sorry, we are unable to retrieve the information for dates provided.")


def get_minimum_maximum_average_temperature(chosen_city, weather_for_dates, endpoint):
    lowest_temp = find_min_val_from_dict(weather_for_dates)
    highest_temp = find_max_val_from_dict(weather_for_dates)
    avg_temp_for_dates = find_avg_val_from_dict(weather_for_dates)


    if endpoint == "history":
        history = (
            f"The weather \U0001F308 last year on the same dates in {chosen_city} was an average of {avg_temp_for_dates}°C, with "
            f"the lowest being {lowest_temp}°C and the highest being {highest_temp}°C.")
        print(
            f" The weather \U0001F308 last year on the same dates in {chosen_city} was an average of {avg_temp_for_dates}°C, with "
            f"the lowest being {lowest_temp}°C and the highest being {highest_temp}°C.")
        return history
    else:
        future = (
            f"The predicted weather \U0001F308 for {chosen_city} on the selected dates will be an average of "
            f"{avg_temp_for_dates}°C, with "
            f"the lowest being {lowest_temp}°C and the highest being {highest_temp}°C.")
        print(
            f"The predicted weather \U0001F308 for {chosen_city} on the selected dates will be an average of "
            f"{avg_temp_for_dates}°C, with "
            f"the lowest being {lowest_temp}°C and the highest being {highest_temp}°C.")
        return future


def find_min_val_from_dict(min_val_to_find):
    val = min_val_to_find
    # using the .get() method will extract any value after the text 'average_temp' in the dictionary passed in
    res = [min_val_to_find.get('average_temp', None) for min_val_to_find in val]
    return min(res)


def find_max_val_from_dict(max_val_to_find):
    val = max_val_to_find
    res = [max_val_to_find.get('average_temp', None) for max_val_to_find in val]
    return max(res)


def find_avg_val_from_dict(avg_val_to_find):
    val = avg_val_to_find
    res = [avg_val_to_find.get('average_temp', None) for avg_val_to_find in val]
    average_temp_for_dates = return_average_number(res)
    return average_temp_for_dates


def return_average_number(avg_val_to_find):
    # round the average to 1 decimal place, seeing the message average of 8.16666666 °C is not as informative as 8.2
    return round(sum(avg_val_to_find) / len(avg_val_to_find), 1)


