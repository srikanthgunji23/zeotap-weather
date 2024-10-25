import requests
import time
from datetime import datetime
from database import create_table, insert_daily_summary
import threading

API_KEY = '63a90ae96d390ec37d6c1252f5a86e1a'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
UPDATE_INTERVAL = 300  # in seconds (5 minutes)

class WeatherMonitor:
    def __init__(self):
        create_table()
        self.daily_data = {}
        self.alert_threshold = 35  # Celsius
        self.alerts = []

    def start_monitoring(self):
        threading.Thread(target=self.monitor_weather).start()

    def monitor_weather(self):
        while True:
            for city in CITIES:
                weather_data = self.get_weather_data(city)
                if weather_data:
                    self.process_weather_data(weather_data)
            self.check_daily_summary()
            time.sleep(UPDATE_INTERVAL)

    def get_weather_data(self, city):
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        return response.json() if response.status_code == 200 else None

    def process_weather_data(self, weather_data):
        dt = datetime.fromtimestamp(weather_data['dt'])
        date_str = dt.strftime('%Y-%m-%d')
        temp = weather_data['main']['temp']
        main_condition = weather_data['weather'][0]['main']

        if date_str not in self.daily_data:
            self.daily_data[date_str] = {'total_temp': 0, 'count': 0, 'max_temp': float('-inf'), 'min_temp': float('inf'), 'conditions': {}}

        self.daily_data[date_str]['total_temp'] += temp
        self.daily_data[date_str]['count'] += 1
        self.daily_data[date_str]['max_temp'] = max(self.daily_data[date_str]['max_temp'], temp)
        self.daily_data[date_str]['min_temp'] = min(self.daily_data[date_str]['min_temp'], temp)
        self.daily_data[date_str]['conditions'][main_condition] = self.daily_data[date_str]['conditions'].get(main_condition, 0) + 1

        if temp > self.alert_threshold:
            self.alerts.append(f"Alert: {city} temperature exceeds {self.alert_threshold}°C")

    def check_daily_summary(self):
        for date, data in self.daily_data.items():
            if data['count'] > 0:
                avg_temp = data['total_temp'] / data['count']
                dominant_condition = max(data['conditions'], key=data['conditions'].get)
                summary = {'date': date, 'average_temp': avg_temp, 'max_temp': data['max_temp'], 'min_temp': data['min_temp'], 'dominant_condition': dominant_condition}
                insert_daily_summary(summary)

    def get_latest_weather(self):
        return {'daily_summaries': self.daily_data, 'alerts': self.alerts}
