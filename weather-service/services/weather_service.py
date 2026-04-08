import requests
import redis
import json
import dotenv
import os
from fastapi import HTTPException

dotenv.load_dotenv()
api_key =  os.getenv("OPENWEATHERMAP_API_KEY")

cache = redis.Redis(host="localhost", port=6379, db=0)

def get_weather_data(city: str):
    # Check if the weather data for the city is in the cache
    cached_weather = cache.get(city)
    if cached_weather:
        return json.loads(cached_weather)

    # If not in cache, fetch from the external API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        # Store the weather data in the cache for future requests
        cache.set(city, json.dumps(weather_data), ex=3600)  # Cache for 1 hour
        return weather_data
    else:
        raise HTTPException(status_code=404, detail={"error": "City not found or API error"})

def get_cache():
    keys = cache.keys()
    cache_size = cache.dbsize()
    stats = {
        "cache_size": cache_size,
        "cached_cities": [key.decode("utf-8") for key in keys]
    }
    return stats