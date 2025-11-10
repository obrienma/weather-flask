# ============== scheduler.py ==============
from apscheduler.schedulers.background import BackgroundScheduler
from data_fetcher import WeatherFetcher
from config import Config

def start_scheduler(app):
    """Start background scheduler for periodic data fetching"""
    scheduler = BackgroundScheduler()

    def fetch_job():
        with app.app_context():
            print("Running scheduled weather fetch...")
            WeatherFetcher.fetch_all_cities()

    # Schedule job to run every FETCH_INTERVAL minutes
    scheduler.add_job(
        func=fetch_job,
        trigger='interval',
        minutes=Config.FETCH_INTERVAL,
        id='weather_fetch_job',
        name='Fetch weather data',
        replace_existing=True
    )

    scheduler.start()
    print(f"Scheduler started - fetching every {Config.FETCH_INTERVAL} minutes")
    return scheduler