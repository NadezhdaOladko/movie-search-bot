# Movie Search Bot

## Описание проекта

Movie Search Bot — Telegram-бот для поиска информации о фильмах с использованием внешнего API.

Пользователь сможет:

- найти фильм по названию;
- получить рейтинг фильма;
- посмотреть описание;
- узнать дату выхода;
- посмотреть постер фильма;
- получить случайную рекомендацию;
- посмотреть топ-10 лучших фильмов;
- сохранить историю запросов.

Проект разрабатывается в рамках финальной работы курса «Основы Python. Часть 2».

## Используемые технологии

- Python 3.13
- pyTelegramBotAPI
- requests
- python-dotenv
- SQLite (как СУБД)
- Peewee (ORM)
- Git
- GitLab

# Используемое API

Для получения информации о фильмах используется API TMDb (The Movie Database).

Документация API:

https://developer.themoviedb.org/

Основные преимущества:

- большая база фильмов;
- высокая скорость работы;
- подробная информация;
- удобный REST API.

# Используемые endpoint

| Endpoint            | Назначение                                         |
|---------------------|----------------------------------------------------|
| `/search/movie`     | Поиск фильма по названию                           |
| `/movie/top_rated`  | Получение списка фильмов с самым высоким рейтингом |
| `/discover/movie`   | Поиск фильмов по заданным критериям                |

# Демонстрация работы с API

Для поиска информации о фильмах используется endpoint:

`GET /search/movie`

### Пример запроса

```text
import requests

BASE_URL = "https://api.themoviedb.org/3"

response = requests.get(
        f"{BASE_URL}/search/movie",
        params={
            "api_key": TMDB_API_KEY,
            "query": movie_name,
            "language": "ru-RU"
        }
    )

print(response.json())
```

### Пример ответа API (сокращённый)

```text
{
  "page": 1,
  "results": [
    {
      "id": 19995,
      "title": "Аватар",
      "overview": "Джейк Салли, бывший морской пехотинец...",
      "release_date": "2009-12-16",
      "vote_average": 7.607
    }
  ],
  "total_pages": 1,
  "total_results": 1
}
```

Из полученного ответа проект использует следующие поля:

- `id` — идентификатор фильма;
- `title` — название фильма;
- `overview` — описание;
- `release_date` — дата выхода;
- `vote_average` — рейтинг фильма;
- `poster_path` — путь к постеру фильма.

Эти данные преобразуются в удобный формат и затем используются для формирования ответа Telegram-бота.

# Команды бота

| Команда  | Описание                   | Endpoint          |
|----------|----------------------------|-------------------|
| /start   | Запуск бота                | —                 |
| /help    | Список доступных команд    | —                 |
| /movie   | Поиск фильма по названию   | `/search/movie`   |
| /history | История поиска             | SQLite            |
| /top10   | Показать 10 лучших фильмов | `/movie/top_rated`|
| /random  | Получить случайный фильм   | `/discover/movie` |

# Структура проекта

```text
python_basic_diploma/
├── api/
    __init__.py
│   └── movie_api.py
├── commands/
    __init__.py
│   ├── help.py
│   ├── history.py
│   ├── movie.py
│   ├── random.py
│   ├── start.py
│   └── top10.py
├──database/
│   ├── __init__.py
│   └── database.py
├── keyboards/
│   ├── __init__.py
│   ├── history_keyboard.py
│   ├── main_menu.py
│   └── movie_keyboard.py
├── states/
│   ├── __init__.py
│   └── movie_states.py
├──utils/
    __init__.py
│   ├── help_message.py
│   └── movie_message.py
├── .env.template
├── .gitignore
├── config.py
├── loader.py
├── main.py 
└── README.md
```

## Алгоритм поиска фильма

1. Пользователь вводит название фильма.
2. Бот отправляет запрос к TMDb API (`/search/movie`).
3. API возвращает список найденных фильмов в формате JSON.
4. Из ответа извлекаются необходимые данные:
   - название;
   - дата выхода;
   - рейтинг;
   - описание.
5. Бот формирует сообщение и отправляет его пользователю.

## Автор

Надежда Оладько

