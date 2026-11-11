from loader import bot
from states.movie_states import MovieStates
from api.movie_api import (
    search_movie,
    get_movie_info,
    search_trailer,
    get_watch_providers_data,
    get_watch_providers
)
from utils.movie_message import send_movie_info
from database.database import Movie
from keyboards.movie_keyboard import gen_movie_markup
from datetime import datetime


def start_movie_search(user_id: int, chat_id: int) -> None:
    """Запускает сценарий поиска фильма и переводит пользователя в состояние ожидания названия."""
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
    movie_name = message.text
    data = search_movie(movie_name)
    try:
        movie = get_movie_info(data)

        send_movie_info(
            message.chat.id,
            movie,
            reply_markup=gen_movie_markup(movie["id"])
        )
        history_record = Movie(
            user_id=message.from_user.id,
            movie_title=movie["title"],
            search_date=datetime.now()
        )
        history_record.save()

    except ValueError as exc:
        bot.reply_to(message, str(exc))

    bot.delete_state(
        message.from_user.id,
        message.chat.id
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("trailer:"))
def handle_trailer_callback(call):
    movie_id = int(call.data.split(":")[1])
    trailer_data = search_trailer(movie_id)
    results = trailer_data["results"]
    if not results:
        bot.send_message(
            call.message.chat.id,
            "❌ Для этого фильма трейлер не найден."
        )
        return

    key = trailer_data["results"][0]["key"]
    link = f"https://www.youtube.com/watch?v={key}"
    bot.send_message(
        call.message.chat.id,
        f"🎬 Трейлер:\n{link}"
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("watch:"))
def handle_watch_callback(call):
    movie_id = int(call.data.split(":")[1])
    providers_data = get_watch_providers_data(movie_id)
    providers = get_watch_providers(providers_data)
    if providers is None:
        bot.send_message(
            call.message.chat.id,
            "❌ Информация о доступности фильма не найдена."
        )
        return

    bot.send_message(
        call.message.chat.id,
        "📺 Фильм можно посмотреть на следующих платформах:\n\n"
        f"{'\n'.join(f'• {provider}' for provider in providers)}"
    )


