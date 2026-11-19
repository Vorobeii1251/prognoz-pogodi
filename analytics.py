def calculate_general_stats(records: list) -> dict:
    if not records:
        return {"message": "Нет данных для анализа"}

    total_temp = sum(r["temperature"] for r in records)
    avg_temp = round(total_temp / len(records), 1)

    hottest = max(records, key=lambda x: x["temperature"])
    coldest = min(records, key=lambda x: x["temperature"])
    windiest = max(records, key=lambda x: x["wind_speed"])

    return {
        "total_records": len(records),
        "avg_temperature": avg_temp,
        "hottest": {
            "city": hottest["city"],
            "temperature": hottest["temperature"]
        },
        "coldest": {
            "city": coldest["city"],
            "temperature": coldest["temperature"]
        },
        "windiest": {
            "city": windiest["city"],
            "wind_speed": windiest["wind_speed"]
        }
    }


def get_city_summary(records: list, city: str) -> dict:

    city_records = [
        r for r in records
        if r["city"].lower() == city.lower()
    ]

    if not city_records:
        return {"message": f"Нет данных по городу {city}"}

    temps = [r["temperature"] for r in city_records]
    avg_temp = round(sum(temps) / len(temps), 1)
    min_temp = min(temps)
    max_temp = max(temps)

    if avg_temp < 0:
        advice = "Одевайтесь тепло, на улице мороз!"
    elif avg_temp <= 15:
        advice = "Прохладно, лучше взять куртку."
    else:
        advice = "Тепло, можно идти налегке."

    return {
        "city": city.capitalize(),
        "checks_count": len(city_records),
        "avg_temperature": avg_temp,
        "min_temperature": min_temp,
        "max_temperature": max_temp,
        "advice": advice
    }