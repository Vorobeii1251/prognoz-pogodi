import aiosqlite

from config import DB_NAME


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS weather_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL,
                description TEXT,
                wind_speed REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_weather_to_db(
        city: str,
        temp: float,
        description: str,
        wind: float
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO weather_history (city, temperature, description, wind_speed) VALUES (?, ?, ?, ?)",
            (city, temp, description, wind)
        )
        await db.commit()


async def get_weather_history() -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT id, city, temperature, description, wind_speed, created_at
            FROM weather_history
            ORDER BY id DESC
        """)
        rows = await cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "city": row[1],
                "temperature": row[2],
                "description": row[3],
                "wind_speed": row[4],
                "created_at": row[5]
            })
        return result


async def delete_city_history(city: str) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "DELETE FROM weather_history WHERE LOWER(city) = LOWER(?)",
            (city,)
        )
        await db.commit()
        return cursor.rowcount