# ============== app.py ==============
from flask import Flask, render_template, jsonify
from models import db, WeatherData
from config import Config
from scheduler import start_scheduler
from data_fetcher import WeatherFetcher
from datetime import datetime, timedelta
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()
    # Fetch initial data if database is empty
    if WeatherData.query.count() == 0:
        print("Fetching initial weather data...")
        WeatherFetcher.fetch_all_cities()

# Start background scheduler
scheduler = start_scheduler(app)

@app.route('/')
def index():
    """Render dashboard"""
    return render_template('dashboard.html', cities=Config.CITIES)

@app.route('/api/current')
def get_current_weather():
    """Get latest weather for all cities"""
    latest_data = []
    for city in Config.CITIES:
        latest = WeatherData.query.filter_by(city=city)\
            .order_by(WeatherData.timestamp.desc()).first()
        if latest:
            latest_data.append(latest.to_dict())

    return jsonify(latest_data)

@app.route('/api/history/<city>')
def get_city_history(city):
    """Get historical data for a specific city (last 24 hours)"""
    since = datetime.utcnow() - timedelta(hours=24)
    history = WeatherData.query.filter(
        WeatherData.city == city,
        WeatherData.timestamp >= since
    ).order_by(WeatherData.timestamp).all()

    return jsonify([record.to_dict() for record in history])

@app.route('/api/stats/<city>')
def get_city_stats(city):
    """Get statistics for a city (last 24 hours)"""
    since = datetime.utcnow() - timedelta(hours=24)

    stats = db.session.query(
        func.avg(WeatherData.temperature).label('avg_temp'),
        func.min(WeatherData.temperature).label('min_temp'),
        func.max(WeatherData.temperature).label('max_temp'),
        func.avg(WeatherData.humidity).label('avg_humidity')
    ).filter(
        WeatherData.city == city,
        WeatherData.timestamp >= since
    ).first()

    return jsonify({
        'city': city,
        'avg_temperature': round(stats.avg_temp, 1) if stats.avg_temp else None,
        'min_temperature': round(stats.min_temp, 1) if stats.min_temp else None,
        'max_temperature': round(stats.max_temp, 1) if stats.max_temp else None,
        'avg_humidity': round(stats.avg_humidity, 1) if stats.avg_humidity else None
    })

@app.route('/api/fetch-now')
def fetch_now():
    """Manually trigger data fetch"""
    WeatherFetcher.fetch_all_cities()
    return jsonify({'status': 'success', 'message': 'Weather data fetched'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
