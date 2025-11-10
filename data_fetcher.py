# ============== data_fetcher.py ==============
import requests
from models import db, WeatherData
from config import Config

class WeatherFetcher:
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    @staticmethod
    def fetch_weather(city):
        """Fetch current weather for a city"""
        try:
            params = {
                'q': city,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': 'metric'  # Use Celsius
            }

            response = requests.get(WeatherFetcher.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract relevant data
            weather_entry = WeatherData(
                city=city,
                temperature=data['main']['temp'],
                feels_like=data['main']['feels_like'],
                humidity=data['main']['humidity'],
                pressure=data['main']['pressure'],
                wind_speed=data['wind']['speed'],
                description=data['weather'][0]['description']
            )

            return weather_entry

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city}: {e}")
            return None

    @staticmethod
    def fetch_all_cities():
        """Fetch weather for all configured cities"""
        results = []
        for city in Config.CITIES:
            weather = WeatherFetcher.fetch_weather(city)
            if weather:
                db.session.add(weather)
                results.append(weather)

        db.session.commit()
        print(f"Fetched weather for {len(results)} cities")
        return results
