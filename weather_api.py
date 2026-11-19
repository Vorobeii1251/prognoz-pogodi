import asyncio
import requests

from config import API_KEY, OPENWEATHER_URL


async def fetch_weather_from_api(city: str) -> dict | None:
    params: dict = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = await asyncio.to_thread(
            requests.get, OPENWEATHER_URL, params=params, timeout=5
        )
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }
