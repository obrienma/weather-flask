# ============== config.py ==============
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get free API key from: https://openweathermap.org/api
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '3d5a828303a292b5c9b38b7e0032da16')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///weather.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cities to track (add more as needed)
    # 'London', 'New York', 'Tokyo', 'Sydney', 'Paris',
    CITIES = ['Vancouver', 'Calgary', 'Toronto', 'Whitehorse']
    # Fetch interval in minutes
    FETCH_INTERVAL = 60
