import requests
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

def current_weather_req(city,country):

    url = "https://api.weatherbit.io/v2.0/current"
    api_key = os.getenv('API_KEY')

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



current_weather_req('Cavite','PH')


