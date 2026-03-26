from fastapi import APIRouter
from services.weather_service import get_weather_data

router = APIRouter()

@router.get("/weather/{city}")
def get_weather(city: str):
    return get_weather_data(city)