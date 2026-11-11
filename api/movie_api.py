import requests
from config import TMDB_API_KEY
import random
from datetime import datetime

BASE_URL: str = "https://api.themoviedb.org/3"
IMAGE_BASE_URL: str = "https://image.tmdb.org/t/p/w500"


def search_movie(movie_name: str) -> dict:
    """
        Выполняет поиск фильма по названию через API TMDb.

        Args:
            movie_name: Название фильма.

        Returns:
            Ответ API в формате JSON.
        """
    response = requests.get(
        f"{BASE_URL}/search/movie",
        params={
            "api_key": TMDB_API_KEY,
            "query": movie_name,
            "language": "ru-RU"
        }
    )

    return response.json()


def get_movie_info(response: dict) -> dict:
    """
        Извлекает основную информацию о первом найденном фильме.

        Args:
            response: Ответ API TMDb.

        Returns:
            Словарь с информацией о фильме:
            id, title, release_date, rating, overview, poster.

        Raises:
            ValueError: Если фильм не найден.
        """
    if response["results"]:
        movie = response["results"][0]
        release_date = datetime.strptime(
            movie["release_date"], "%Y-%m-%d"
        ).strftime("%d.%m.%Y")
        poster = (
            IMAGE_BASE_URL + movie["poster_path"]
            if movie["poster_path"]
            else None
        )
        return {
            "id": movie["id"],
            "title": movie["title"],
            "release_date": release_date,
            "rating": movie["vote_average"],
            "overview": movie["overview"],
            "poster": poster
        }
    raise ValueError("❌ Фильм не найден. Попробуйте ввести другое название.")


def search_top_10() -> dict:
    """
        Получает список фильмов с самым высоким рейтингом.

        Returns:
            Ответ API TMDb в формате JSON.
        """
    response = requests.get(
        f"{BASE_URL}/movie/top_rated",
        params={
            "api_key": TMDB_API_KEY,
            "language": "ru-RU",
            "page": 1,
        }
    )

    return response.json()


def get_top_10_movies(response: dict) -> list[tuple[str, int]]:
    """
    Формирует список названий десяти лучших фильмов.

    Args:
        response: Ответ API TMDb.

    Returns:
        Список из десяти названий фильмов.
    """
    return [
        (movie["title"],
         movie["id"])
        for movie in response["results"][:10]
    ]


def search_random_movie() -> dict:
    """
    Получает список фильмов со случайной страницы TMDb.

    Returns:
        Ответ API TMDb в формате JSON.
    """
    while True:
        page = random.randint(1, 500)

        response = requests.get(
            f"{BASE_URL}/discover/movie",
            params={
                "api_key": TMDB_API_KEY,
                "language": "ru-RU",
                "page": page,
                "sort_by": "vote_average.desc",
                "vote_count.gte": 1000,
            }
        )

        data = response.json()

        if data["results"]:
            return data


def get_random_movie(response: dict) -> dict:
    """
    Выбирает случайный фильм из списка и возвращает
    результат поиска этого фильма.

    Args:
        response: Ответ API TMDb.

    Returns:
        Ответ API TMDb с информацией о случайном фильме.
    """
    movie = random.choice(response["results"])
    return search_movie(movie["title"])


def search_trailer(movie_id: int) -> dict:
    """
    Получает список видеоматериалов фильма (трейлеры, тизеры и др.).

    Args:
        movie_id: Идентификатор фильма в TMDb.

    Returns:
        Ответ API TMDb в формате JSON.
    """
    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}/videos",
        params={
            "api_key": TMDB_API_KEY,
            "language": "ru-RU"
        }
    )

    return response.json()


def get_watch_providers_data(movie_id: int) -> dict:
    """
    Получает список онлайн-платформ, на которых доступен фильм.

    Args:
        movie_id: Идентификатор фильма в TMDb.

    Returns:
        Ответ API TMDb в формате JSON.
    """
    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}/watch/providers",
        params={
            "api_key": TMDB_API_KEY
        }
    )

    return response.json()


def get_watch_providers(response: dict) -> list[str] | None:
    """
    Извлекает список онлайн-платформ, на которых доступен фильм.

    Последовательно проверяет Казахстан, Россию и США.
    Если фильм доступен в нескольких странах, объединяет список
    платформ без повторений.

    Args:
        response: Ответ API TMDb.

    Returns:
        Список (providers), где:
            providers — строки с названием платформ;

        Если информации о доступности нет, возвращает None.
    """
    results = response["results"]
    countries = ["KZ", "RU", "US"]
    providers = []
    for country in countries:
        if country not in results:
            continue

        country_data = results[country]
        for provider in country_data.get("flatrate", []):
            provider_name = provider["provider_name"]
            if provider_name not in providers:
                providers.append(provider_name)

    if not providers:
        return None

    return providers


def search_movie_by_id(movie_id: int) -> dict:
    """
    Получает подробную информацию о фильме по его id.

    Args:
        movie_id: Идентификатор фильма в TMDb.

    Returns:
        Словарь с информацией о фильме.
    """
    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        params={
            "api_key": TMDB_API_KEY,
            "language": "ru-RU"
        }
    )

    movie = response.json()
    release_date = datetime.strptime(
        movie["release_date"], "%Y-%m-%d"
    ).strftime("%d.%m.%Y")
    poster = (
        IMAGE_BASE_URL + movie["poster_path"]
        if movie["poster_path"]
        else None
    )

    return {
        "id": movie["id"],
        "title": movie["title"],
        "release_date": release_date,
        "rating": movie["vote_average"],
        "overview": movie["overview"],
        "poster": poster
    }