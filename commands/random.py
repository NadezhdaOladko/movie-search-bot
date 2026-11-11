from loader import bot
from utils.movie_message import send_movie_info
from api.movie_api import (
    search_random_movie,
    get_random_movie,
    get_movie_info,
    search_trailer,
    get_watch_providers_data,
    get_watch_providers
)
from database.database import Movie
from keyboards.movie_keyboard import gen_movie_markup
from datetime import datetime


def send_random_movie_impl(chat_id: int, user_id: int) -> None:
    """Отправляет пользователю информацию о случайно выбранном фильме и сохраняет запрос в историю."""
    bot.send_message(
        chat_id,
        "🎲 Случайный выбор!\n\n"
        "Возможно, именно этот фильм станет вашим следующим любимым."
    )
    movie = get_movie_info(get_random_movie(search_random_movie()))
    send_movie_info(
        chat_id,
        movie,
        reply_markup=gen_movie_markup(movie["id"]))
    history_record = Movie(
        user_id=user_id,
        movie_title=movie["title"],
        search_date=datetime.now()
    )
    history_record.save()


@bot.message_handler(commands=["random"])
def send_random_movie(message):
    send_random_movie_impl(message.chat.id, message.from_user.id)


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
    data = get_watch_providers_data(movie_id)
    providers = get_watch_providers(data)
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
