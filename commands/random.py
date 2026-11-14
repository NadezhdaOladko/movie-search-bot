from datetime import datetime

from sqlalchemy import insert

from loader import bot
from api.movie_api import (
    search_random_movie,
    get_random_movie,
    get_movie_info,
)
from utils.movie_message import send_movie_info
from database.database import Movie, Session
from keyboards.movie_keyboard import gen_movie_markup


def send_random_movie_impl(chat_id: int, user_id: int) -> None:
    """Отправляет случайный фильм и сохраняет его в историю."""
    bot.send_message(
        chat_id,
        "🎲 Случайный выбор!\n\n"
        "Возможно, именно этот фильм станет вашим следующим любимым."
    )

    try:
        response = search_random_movie()
        movie_data = get_random_movie(response)
        movie = get_movie_info(movie_data)

        send_movie_info(
            chat_id,
            movie,
            reply_markup=gen_movie_markup(movie["id"])
        )

        with Session() as session:
            session.execute(
                insert(Movie).values(
                    user_id=user_id,
                    movie_title=movie["title"],
                    search_date=datetime.now()
                )
            )
            session.commit()
    except ValueError as exc:
        bot.send_message(chat_id, str(exc))


@bot.message_handler(commands=["random"])
def send_random_movie(message):
    send_random_movie_impl(
        message.chat.id,
        message.from_user.id
    )