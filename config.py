import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value or not value.strip():
        raise RuntimeError(f"Не задана обязательная переменная окружения: {name}")

    return value.strip()


BOT_TOKEN = get_required_env("BOT_TOKEN")
TMDB_API_KEY = get_required_env("TMDB_API_KEY")