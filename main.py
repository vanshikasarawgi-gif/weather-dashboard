import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timezone
import pytz
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load environment variables
load_dotenv()

# Coordinates for New Delhi
LAT = 28.613939
LONG = 77.209023

api_key = os.getenv("API_KEY")

url = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    "lat": LAT,
    "lon": LONG,
    "appid": api_key,
    "cnt": 9
}

response = requests.get(url=url, params=parameters)
response.raise_for_status()
data = response.json()

forecast_list = data['list']
weather_data = []

# --- Create DataFrame ---
for item in forecast_list:
    utc_time = datetime.fromtimestamp(item['dt'], tz=timezone.utc)
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))

    weather_data.append({
        'time': ist_time,
        'temp': item['main']['temp'],
        'min_temp': item['main']['temp_min'],
        'max_temp': item['main']['temp_max'],
        'pressure': item['main']['pressure'],
        'humidity': item['main']['humidity'],
        'sea_level': item['main'].get('sea_level', None)
    })

df = pd.DataFrame(weather_data)



# Convert Kelvin to Celsius
df['temp'] = df['temp'] - 273.15
df['min_temp'] = df['min_temp'] - 273.15
df['max_temp'] = df['max_temp'] - 273.15

# Convert to hour format (AM/PM)
df['hour'] = df['time'].dt.strftime('%I %p')




#  --- Streamlit Layout ---
st.title("🌤️ Weather Dashboard - New Delhi")
st.write("""
Welcome to the **New Delhi Weather Forecast Dashboard**!  
This dashboard visualizes live weather data from the **OpenWeatherMap API**, showing temperature, humidity, pressure, and other atmospheric parameters for the next few hours.
""")

st.markdown("---")
st.subheader("📋 Raw Forecast Data")
st.write("Here’s a preview of the forecasted weather data fetched from the API:")
st.dataframe(df[['hour', 'temp', 'min_temp', 'max_temp', 'pressure', 'humidity']])



#  --- Plot 1: Temperature vs Time ---
st.markdown("---")
st.header("🌡️ Temperature vs Time")
st.write("This line graph shows how the temperature changes across different time slots in the forecast period.")
fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(data=df, x='hour', y='temp', marker='o', ax=ax, color='purple')
ax.set_xlabel('Time (IST)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Temperature Forecast (Next Few Hours)')
st.pyplot(fig)



#  --- Plot 2: Temperature vs Humidity ---
st.markdown("---")
st.header("💧 Temperature and Humidity Over Time")
st.write("This chart compares **temperature and humidity** trends together to show how they vary simultaneously over time.")
fig2, ax2 = plt.subplots(figsize=(8,4))
sns.lineplot(data=df, x='hour', y='temp', marker='o', label='Temperature (°C)', ax=ax2, color='red')
sns.lineplot(data=df, x='hour', y='humidity', marker='s', label='Humidity (%)', ax=ax2, color='royalblue')
ax2.set_xlabel('Time (IST)')
ax2.set_ylabel('Value')
ax2.legend()
ax2.set_title('Temperature and Humidity Over Time')
st.pyplot(fig2)



#  --- Plot 3: Min vs Max Temp ---
st.markdown("---")
st.header("🌤️ Min vs Max Temperature Over Time")
st.write("This graph compares the **minimum and maximum temperatures** predicted for each forecasted time slot.")
fig3, ax3 = plt.subplots(figsize=(8,4))
sns.lineplot(data=df, x='hour', y='min_temp', marker='o', ax=ax3, label="Min Temp (°C)", color='skyblue')
sns.lineplot(data=df, x='hour', y='max_temp', marker='o', ax=ax3, label="Max Temp (°C)", color='coral')
ax3.set_xlabel('Time (IST)')
ax3.set_ylabel('Temperature (°C)')
ax3.legend()
ax3.set_title('Min vs Max Temperature Forecast')
st.pyplot(fig3)



#  --- Plot 4: Average Temperature ---
st.markdown("---")
st.header("📊 Average Temperature per Time Slot")
st.write("A bar chart representing the **average temperature** for each time slot.")
fig4, ax4 = plt.subplots(figsize=(8,4))
sns.barplot(data=df, x='hour', y='temp', color='coral', ax=ax4)
ax4.set_xlabel('Time (IST)')
ax4.set_ylabel('Temperature (°C)')
ax4.set_title('Average Temperature by Hour')
st.pyplot(fig4)



#  --- Plot 5: Temperature vs Humidity Scatter ---
st.markdown("---")
st.header("🔵 Temperature vs Humidity Scatter Plot")
st.write("This scatter plot shows the **relationship between temperature and humidity**, with colors indicating the time of day.")
fig5, ax5 = plt.subplots(figsize=(6,4))
sns.scatterplot(data=df, x='temp', y='humidity', hue='hour', palette='coolwarm', s=80, ax=ax5)
ax5.set_title("Relationship Between Temperature & Humidity")
st.pyplot(fig5)



#  --- Plot 6: Correlation Heatmap ---
st.markdown("---")
st.header("🔥 Correlation Heatmap")
st.write("The heatmap displays **correlations** between different weather parameters such as temperature, humidity, and pressure.")
corr = df.corr(numeric_only=True)
fig6, ax6 = plt.subplots(figsize=(8, 4))
sns.heatmap(data=corr, cmap='coolwarm', linewidths=1, linecolor='black', annot=True, fmt=".2f", ax=ax6)
ax6.set_title("Heatmap Showing Correlation Between Weather Parameters")
st.pyplot(fig6)



#  --- Plot 7: Pressure Distribution ---
st.markdown("---")
st.header("🌪️ Pressure Distribution by Hour")
st.write("A line graph showing **pressure variation** throughout the forecasted hours.")
fig7, ax7 = plt.subplots(figsize=(8,4))
sns.lineplot(data=df, x='hour', y='pressure', color='green', ax=ax7)
ax7.set_xlabel('Hour')
ax7.set_ylabel('Pressure (hPa)')
ax7.set_title('Pressure Distribution by Hour')
st.pyplot(fig7)



#  --- Plot 8: Pairplot ---
st.markdown("---")
st.header("🔍 Pairplot of Weather Variables")
st.write("The pairplot visualizes pairwise relationships between variables like **temperature, humidity, pressure, and sea level**.")

cols = ['temp', 'sea_level', 'humidity', 'pressure']
df_pair = df[cols + ['hour']].dropna(how='all', subset=['sea_level'])


df_pair = df_pair.rename(columns={
    'temp': 'Temperature (°C)',
    'humidity': 'Humidity (%)',
    'pressure': 'Pressure (hPa)',
    'sea_level': 'Sea Level (hPa)'
})

pairplot_fig = sns.pairplot(
    df_pair,
    hue='hour',
    palette='Set2',
    diag_kind='kde',
    plot_kws={'alpha': 0.8, 's': 60}
)

pairplot_fig.fig.suptitle("Pairplot of Weather Variables by Hour", y=1.02)
pairplot_fig._legend.set_title("Time (IST)")

st.pyplot(pairplot_fig)




st.markdown("---")
st.info(" Dashboard built using **Python, Streamlit, Seaborn, and OpenWeatherMap API**.")
st.caption("Developed by Vanshika Sarawgi | Data fetched live from OpenWeatherMap ")
