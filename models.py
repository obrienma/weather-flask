# ============== models.py ==============
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Weather metrics
    temperature = db.Column(db.Float)  # Celsius
    feels_like = db.Column(db.Float)
    humidity = db.Column(db.Integer)  # Percentage
    pressure = db.Column(db.Integer)  # hPa
    wind_speed = db.Column(db.Float)  # m/s
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<WeatherData {self.city} at {self.timestamp}>'

    def to_dict(self):
        return {
            'city': self.city,
            'timestamp': self.timestamp.isoformat(),
            'temperature': self.temperature,
            'feels_like': self.feels_like,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'description': self.description
        }