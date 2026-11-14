from datetime import datetime

from sqlalchemy import insert

from loader import bot
from states.movie_states import MovieStates
from api.movie_api import (
    search_movie,
    get_movie_info,
    search_trailer,
    get_watch_providers_data,
    get_watch_providers,
)
from utils.movie_message import send_movie_info
from database.database import Movie, Session
from keyboards.movie_keyboard import gen_movie_markup


def start_movie_search(user_id: int, chat_id: int) -> None:
    """Запускает поиск фильма."""
    bot.send_message(
        chat_id,
        "Введите название фильма, который хотите найти."
    )
    bot.set_state(
        user_id,
        MovieStates.waiting_movie_name,
        chat_id
    )


@bot.message_handler(commands=["movie"])
def reply_to_movie(message):
    start_movie_search(message.from_user.id, message.chat.id)


@bot.message_handler(state=MovieStates.waiting_movie_name)
def display_info(message):
    movie_name = (message.text or "").strip()

    try:
        if not movie_name:
            bot.reply_to(
                message,
                "Введите название фильма текстом."
            )
            return

        data = search_movie(movie_name)
        movie = get_movie_info(data)

        send_movie_info(
            message.chat.id,
            movie,
            reply_markup=gen_movie_markup(movie["id"])
        )

        with Session() as session:
            session.execute(
                insert(Movie).values(
                    user_id=message.from_user.id,
                    movie_title=movie["title"],
                    search_date=datetime.now()
                )
            )
            session.commit()
    except ValueError as exc:
        bot.reply_to(message, str(exc))
    finally:
        bot.delete_state(
            message.from_user.id,
            message.chat.id
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("trailer:"))
def handle_trailer_callback(call):
    movie_id = int(call.data.split(":")[1])

    try:
        trailer_data = search_trailer(movie_id)
        results = trailer_data.get("results", [])
        if not results:
            bot.send_message(
                call.message.chat.id,
                "❌ Для этого фильма трейлер не найден."
            )
            return

        key = results[0].get("key")
        if not key:
            bot.send_message(
                call.message.chat.id,
                "❌ Ссылка на трейлер отсутствует."
            )
            return

        link = f"https://www.youtube.com/watch?v={key}"

        bot.send_message(
            call.message.chat.id,
            f"🎬 Трейлер:\n{link}"
        )
    except ValueError as exc:
        bot.send_message(call.message.chat.id, str(exc))


@bot.callback_query_handler(func=lambda call: call.data.startswith("watch:"))
def handle_watch_callback(call):
    movie_id = int(call.data.split(":")[1])

    try:
        providers_data = get_watch_providers_data(movie_id)
        providers = get_watch_providers(providers_data)
        if not providers:
            bot.send_message(
                call.message.chat.id,
                "❌ Информация о доступности фильма не найдена."
            )
            return

        providers_list = "\n".join(
            f"• {provider}" for provider in providers
        )

        bot.send_message(
            call.message.chat.id,
            "📺 Фильм можно посмотреть на следующих платформах:\n\n"
            f"{providers_list}"
        )
    except ValueError as exc:
        bot.send_message(call.message.chat.id, str(exc))
