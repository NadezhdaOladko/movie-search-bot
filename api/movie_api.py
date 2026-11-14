import random
from datetime import datetime

import requests

from config import TMDB_API_KEY


BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
REQUEST_TIMEOUT = 10
MAX_RANDOM_ATTEMPTS = 5


def _make_request(endpoint: str, params: dict | None = None) -> dict:
    """Выполняет GET-запрос к TMDB API."""
    request_params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU",
    }
    if params:
        request_params.update(params)

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint.lstrip('/')}",
            params=request_params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise ValueError(
            "❌ Получен некорректный ответ от TMDB."
        ) from exc
    except requests.RequestException as exc:
        raise ValueError(
            "❌ Не удалось получить данные от TMDB. Попробуйте позже."
        ) from exc


def _format_movie(movie: dict) -> dict:
    """Форматирует данные фильма для отображения пользователю."""
    release_date = movie.get("release_date")

    if release_date:
        try:
            release_date = datetime.strptime(
                release_date, "%Y-%m-%d"
            ).strftime("%d.%m.%Y")
        except ValueError:
            release_date = "Неизвестно"
    else:
        release_date = "Неизвестно"

    poster_path = movie.get("poster_path")

    return {
        "id": movie["id"],
        "title": movie.get("title", "Без названия"),
        "release_date": release_date,
        "rating": movie.get("vote_average", 0),
        "overview": movie.get("overview") or "Описание отсутствует.",
        "poster": f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None,
    }


def search_movie(movie_name: str) -> dict:
    """Ищет фильмы по названию."""
    return _make_request(
        "search/movie",
        {"query": movie_name},
    )


def get_movie_info(response: dict) -> dict:
    """Извлекает информацию о первом найденном фильме."""
    results = response.get("results", [])

    if not results:
        raise ValueError(
            "❌ Фильм не найден. Попробуйте ввести другое название.\n\n"
            "Чтобы начать новый поиск, отправьте команду /movie или воспользуйтесь главным меню."
        )

    return _format_movie(results[0])


def search_top_10() -> dict:
    """Получает список фильмов с самым высоким рейтингом."""
    return _make_request(
        "movie/top_rated",
        {"page": 1},
    )


def get_top_10_movies(response: dict) -> list[tuple[str, int]]:
    """Формирует список названий десяти лучших фильмов."""
    return [
        (movie["title"], movie["id"])
        for movie in response.get("results", [])[:10]
    ]


def search_random_movie() -> dict:
    """Получает список фильмов со случайной страницы TMDB."""
    for _ in range(MAX_RANDOM_ATTEMPTS):
        page = random.randint(1, 500)
        response = _make_request(
            "discover/movie",
            {
                "page": page,
                "sort_by": "vote_average.desc",
                "vote_count.gte": 1000,
            },
        )

        if response.get("results"):
            return response

    raise ValueError(
        "❌ Не удалось подобрать случайный фильм. Попробуйте позже."
    )


def get_random_movie(response: dict) -> dict:
    """Выбирает случайный фильм и получает его данные по ID."""
    results = response.get("results", [])

    if not results:
        raise ValueError("❌ Список фильмов пуст.")

    movie = random.choice(results)
    movie_data = _make_request(f"movie/{movie['id']}")

    return {"results": [movie_data]}


def search_trailer(movie_id: int) -> dict:
    """Получает видеоматериалы фильма."""
    return _make_request(f"movie/{movie_id}/videos")


def get_watch_providers_data(movie_id: int) -> dict:
    """Получает информацию о платформах для просмотра фильма."""
    return _make_request(f"movie/{movie_id}/watch/providers")


def get_watch_providers(response: dict) -> list[str] | None:
    """Извлекает платформы просмотра для Казахстана, России и США."""
    results = response.get("results", {})
    countries = ["KZ", "RU", "US"]
    provider_types = ["flatrate", "free", "ads", "rent", "buy"]
    providers = []

    for country in countries:
        country_data = results.get(country, {})

        for provider_type in provider_types:
            for provider in country_data.get(provider_type, []):
                name = provider.get("provider_name")

                if name and name not in providers:
                    providers.append(name)

    return providers or None


def search_movie_by_id(movie_id: int) -> dict:
    """Получает и форматирует информацию о фильме по ID."""
    movie = _make_request(f"movie/{movie_id}")
    return _format_movie(movie)