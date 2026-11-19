
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env в корне проекта
load_dotenv()

# Читаем значения из окружения (вторым аргументом можно задать значение по умолчанию)
DB_NAME = os.getenv("DB_NAME", "weather.db")
OPENWEATHER_URL = os.getenv(
    "OPENWEATHER_URL",
    "https://api.openweathermap.org/data/2.5/weather"
)

# Секретный ключ API — для него не ставим значение по умолчанию
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Проверяем при запуске, что ключ действительно задан (принцип Fail Fast)
if not API_KEY:
    raise ValueError(
        "Не найден OPENWEATHER_API_KEY! "
        "Создайте файл .env в корне проекта и укажите в нём ваш ключ API."
    )
