import React, { useState, useEffect } from 'react';
import { Cloud, CloudRain, Sun, Wind, Droplets, Eye, Gauge, MapPin, Search } from 'lucide-react';

export default function WeatherApp() {
  const [city, setCity] = useState('Vancouver');
  const [searchInput, setSearchInput] = useState('');
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchWeather = async (cityName) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=demo&units=metric`
      );

      if (!response.ok) {
        throw new Error('City not found');
      }

      const data = await response.json();
      setWeather(data);
      setCity(cityName);
    } catch (err) {
      setError('Unable to fetch weather data. Please try again.');
      // Set demo data for demonstration
      setWeather({
        name: cityName,
        sys: { country: 'CA' },
        main: {
          temp: 12,
          feels_like: 10,
          humidity: 75,
          pressure: 1013
        },
        weather: [{
          main: 'Clouds',
          description: 'overcast clouds'
        }],
        wind: { speed: 3.5 },
        visibility: 10000
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather(city);
  }, []);

  const handleSearch = () => {
    if (searchInput.trim()) {
      fetchWeather(searchInput);
      setSearchInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const getWeatherIcon = (weatherMain) => {
    switch (weatherMain?.toLowerCase()) {
      case 'clear':
        return <Sun className="w-24 h-24 text-yellow-400" />;
      case 'rain':
      case 'drizzle':
        return <CloudRain className="w-24 h-24 text-blue-400" />;
      case 'clouds':
        return <Cloud className="w-24 h-24 text-gray-400" />;
      default:
        return <Cloud className="w-24 h-24 text-gray-400" />;
    }
  };

  const getBackgroundGradient = (weatherMain) => {
    switch (weatherMain?.toLowerCase()) {
      case 'clear':
        return 'from-blue-400 via-blue-300 to-blue-200';
      case 'rain':
      case 'drizzle':
        return 'from-gray-600 via-gray-500 to-gray-400';
      case 'clouds':
        return 'from-gray-500 via-gray-400 to-gray-300';
      default:
        return 'from-blue-500 via-blue-400 to-blue-300';
    }
  };

  if (loading && !weather) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
        <div className="text-white text-2xl">Loading weather...</div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br ${getBackgroundGradient(weather?.weather[0]?.main)} p-4 md:p-8`}>
      <div className="max-w-4xl mx-auto">
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative">
            <input
              type="text"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search for a city..."
              className="w-full px-6 py-4 pr-12 rounded-2xl bg-white/20 backdrop-blur-md text-white placeholder-white/70 text-lg focus:outline-none focus:ring-2 focus:ring-white/50"
            />
            <button
              onClick={handleSearch}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-white hover:scale-110 transition-transform"
            >
              <Search className="w-6 h-6" />
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-500/20 backdrop-blur-md rounded-xl text-white text-center">
            {error}
          </div>
        )}

        {/* Main Weather Card */}
        <div className="bg-white/20 backdrop-blur-md rounded-3xl p-8 shadow-2xl mb-6">
          <div className="flex items-center gap-2 mb-6">
            <MapPin className="w-5 h-5 text-white" />
            <h1 className="text-3xl font-bold text-white">
              {weather?.name}, {weather?.sys?.country}
            </h1>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="flex items-center gap-8">
              {getWeatherIcon(weather?.weather[0]?.main)}
              <div>
                <div className="text-7xl font-bold text-white">
                  {Math.round(weather?.main?.temp)}°
                </div>
                <div className="text-xl text-white/90 capitalize mt-2">
                  {weather?.weather[0]?.description}
                </div>
              </div>
            </div>

            <div className="text-white/90 text-lg">
              <div>Feels like {Math.round(weather?.main?.feels_like)}°</div>
            </div>
          </div>
        </div>

        {/* Weather Details Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 text-white">
            <div className="flex items-center gap-2 mb-2">
              <Wind className="w-5 h-5" />
              <div className="text-sm opacity-80">Wind Speed</div>
            </div>
            <div className="text-2xl font-bold">{weather?.wind?.speed} m/s</div>
          </div>

          <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 text-white">
            <div className="flex items-center gap-2 mb-2">
              <Droplets className="w-5 h-5" />
              <div className="text-sm opacity-80">Humidity</div>
            </div>
            <div className="text-2xl font-bold">{weather?.main?.humidity}%</div>
          </div>

          <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 text-white">
            <div className="flex items-center gap-2 mb-2">
              <Eye className="w-5 h-5" />
              <div className="text-sm opacity-80">Visibility</div>
            </div>
            <div className="text-2xl font-bold">{(weather?.visibility / 1000).toFixed(1)} km</div>
          </div>

          <div className="bg-white/20 backdrop-blur-md rounded-2xl p-6 text-white">
            <div className="flex items-center gap-2 mb-2">
              <Gauge className="w-5 h-5" />
              <div className="text-sm opacity-80">Pressure</div>
            </div>
            <div className="text-2xl font-bold">{weather?.main?.pressure} hPa</div>
          </div>
        </div>
      </div>
    </div>
  );
}