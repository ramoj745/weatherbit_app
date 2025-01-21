import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

def current_weather_req(city,country):

    url = "https://api.weatherbit.io/v2.0/current"

    param = {
        'city': f'{city}',
        'country': f'{country}',
        'key': api_key
    }

    response = requests.get(url, params=param)

    weather_data = response.json()

    for weather in weather_data['data']:
        timezone = weather['timezone']
        last_observed = weather['ob_time']
        wind_speed = weather['wind_spd']
        temp = weather['temp']
        temp_feelslike = weather['app_temp']
        cloud_cvrg = weather['clouds']
        precipitation = weather['precip']
        curr_weather = weather['weather']['description']

    return (timezone, last_observed, wind_speed, temp, temp_feelslike, cloud_cvrg, precipitation,curr_weather)

def daily_weather(city,country):

    url = "https://api.weatherbit.io/v2.0/forecast/daily"

    param = {
        'city': f'{city}',
        'country': f'{country}',
        'key': api_key
    }

    response = requests.get(url, params=param)

    daily_weather_data = response.json()

    return daily_weather_data






