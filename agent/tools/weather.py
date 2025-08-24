import requests
import os
from datetime import datetime
from typing import Dict, Optional, Union

# Custom exceptions for better error handling
class WeatherAPIError(Exception):
    def __init__(self, message="Weather API error occurred"):
        super().__init__(message)

class CityNotFoundError(Exception):
    def __init__(self, message="City not found in weather data"):
        super().__init__(message)

class WeatherDataUnavailableError(Exception):
    def __init__(self, message="Weather data is temporarily unavailable"):
        super().__init__(message)

# Just to represent a mock API
_FALLBACK_TEMPERATURES = {
    "paris": 18.0,
    "london": 17.0,
    "dhaka": 31.0,
    "amsterdam": 19.5,
    "new york": 22.0,
    "tokyo": 25.0,
    "sydney": 20.0,
    "berlin": 16.0,
    "madrid": 24.0,
    "rome": 26.0,
    "mumbai": 29.0,
    "delhi": 28.0,
    "beijing": 15.0,
    "shanghai": 20.0,
    "los angeles": 23.0,
    "chicago": 12.0,
    "toronto": 8.0,
    "moscow": 5.0,
    "dubai": 35.0,
    "singapore": 30.0
}

def _validate_city_input(city: str) -> str:
    if not isinstance(city, str):
        raise TypeError(f"City must be a string, got {type(city).__name__}")
    
    if not city or not city.strip():
        raise ValueError("City name cannot be empty")
    
    return city.strip()

def _get_weather_from_api(city: str) -> Optional[Dict]:
    
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return None
    
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather" # A dummy API endpoint
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric' 
        }
        
        response = requests.get(base_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp']
            }
        else:
            if response.status_code == 404:
                raise CityNotFoundError(f"City '{city}' not found in weather API")
            else:
                raise WeatherAPIError(f"Weather API returned status code {response.status_code}")
            
    except requests.RequestException as e:
        raise WeatherDataUnavailableError(f"Weather API is currently unavailable: {str(e)}")
    except (KeyError, ValueError) as e:
        raise WeatherAPIError(f"Invalid response from weather API: {str(e)}")

def _get_temperature_from_fallback(city: str) -> float:
    city_lower = city.lower()
    
    if city_lower not in _FALLBACK_TEMPERATURES:
        available_cities = ", ".join(sorted(_FALLBACK_TEMPERATURES.keys()))
        raise CityNotFoundError(
            f"City '{city}' not found in weather database. "
            f"Available cities: {available_cities}"
        )
    
    return _FALLBACK_TEMPERATURES[city_lower]

def get_weather(city: str) -> str:
    try:
        validated_city = _validate_city_input(city)
        try:
            weather_data = _get_weather_from_api(validated_city)
            if weather_data:
                temp = weather_data['temperature']
                # Return temperature with unit
                return f"{int(temp) if temp == int(temp) else temp}°C"
        except (CityNotFoundError, WeatherAPIError, WeatherDataUnavailableError):
            pass
        
        # Fall back to static data
        temp = _get_temperature_from_fallback(validated_city)
        # Return temperature with unit
        return f"{int(temp) if temp == int(temp) else temp}°C"
        
    except (TypeError, ValueError, CityNotFoundError, WeatherAPIError, WeatherDataUnavailableError) as e:
        raise e
    except Exception as e:
        
        raise RuntimeError(f"Unexpected error getting weather for '{city}': {str(e)}")