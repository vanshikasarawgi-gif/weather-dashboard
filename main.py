import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime,timezone
import pytz
import seaborn as sns
import matplotlib.pyplot as plt

load_dotenv()

LAT = 28.613939
LONG = 77.209023

api_key = os.getenv("API_KEY")

url = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {"lat" : LAT,
              "lon" : LONG,
              "appid" : api_key,
              "cnt": 4
              }

response = requests.get(url=url,params=parameters)
response.raise_for_status()
data = response.json()

forecast_list = data['list']

weather_data = []

#create  the dataframe

for item in forecast_list:

    utc_time = datetime.fromtimestamp(item['dt'], tz=timezone.utc)  # UTC timezone-aware
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))   # Convert to IST

    weather_data.append({
        'time': ist_time,
        'temp': item['main']['temp'],
        'min_temp': item['main']['temp_min'],
        'max_temp': item['main']['temp_max'],
        'pressure': item['main']['pressure'],
        'humidity': item['main']['humidity'],
        'sea_level': item['main']['sea_level']
    })

df = pd.DataFrame(weather_data)
print(df)

