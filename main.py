from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from analytics import calculate_general_stats, get_city_summary
from database import (
    init_db,
    save_weather_to_db,
    get_weather_history,
    delete_city_history,
)
from weather_api import fetch_weather_from_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Инициализирует базу данных при старте сервера
    """

    await init_db()
    print("База данных готова к работе!")
    yield


app = FastAPI(title="Асинхронный Метеосервис", lifespan=lifespan)


@app.post("/weather/{city}")
async def check_and_save_weather(city: str):
    """
    Узнает погоду в городе через OpenWeatherMap и сохраняет результат в БД
    """

    weather = await fetch_weather_from_api(city)

    if not weather:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Не удалось получить погоду для города '{city}'. "
                "Проверьте название или API-ключ."
            )
        )

    await save_weather_to_db(
        weather["city"],
        weather["temperature"],
        weather["description"],
        weather["wind_speed"]
    )
    return {
        "message": "Погода получена и сохранена в базу",
        "data": weather
    }


@app.get("/history")
async def read_history():
    """
    Возвращает всю историю сохраненных запросов из базы данных
    """

    records = await get_weather_history()
    return {"total": len(records), "history": records}


@app.delete("/history/{city}")
async def clear_city_history(city: str):
    """
    Удаляет из базы все записи по конкретному городу
    """

    deleted_count = await delete_city_history(city)

    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Записей для города '{city}' в базе не найдено."
        )

    return {
        "message": f"Удалено записей для города '{city}': {deleted_count}"
    }


@app.get("/analytics")
async def get_analytics():
    """
    Возвращает общую статистику по всем сохраненным городам
    """

    records = await get_weather_history()
    return calculate_general_stats(records)


@app.get("/analytics/{city}")
async def get_city_analytics(city: str):
    """
    Возвращает статистику и совет по одежде для конкретного города
    """

    records = await get_weather_history()
    return get_city_summary(records, city)
