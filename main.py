import requests
from dotenv import load_dotenv
import os

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
print(forecast_list)


