from fastapi import APIRouter
from services.weather_service import get_weather_data, get_cache

router = APIRouter()

@router.get("/weather/{city}")
def get_weather(city: str):
    return get_weather_data(city)

@router.get("/cache/stats")
def get_stats():
    return get_cache()