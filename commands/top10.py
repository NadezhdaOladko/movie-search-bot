from loader import bot
from api.movie_api import (
    search_top_10,
    get_top_10_movies,
    search_movie_by_id
)
from utils.movie_message import send_movie_info
from keyboards.movie_keyboard import gen_top10_markup, gen_movie_markup


def show_top10(chat_id: int) -> None:
    """Отправляет пользователю список десяти лучших фильмов TMDb с инлайн-кнопками для выбора фильма."""
    data = search_top_10()
    results = get_top_10_movies(data)
    text = (
            "🏆 Топ-10 фильмов по версии пользователей TMDb\n\n"
            + "\n".join(
        f"{i}. {title}"
        for i, (title, movie_id) in enumerate(results, start=1)
        )
    )
    bot.send_message(
        chat_id,
        text,
        reply_markup=gen_top10_markup(results)
    )
    bot.send_message(
        chat_id,
        "Выберите понравившийся фильм, и я предоставлю подробную информацию о нём."
    )


@bot.message_handler(commands=['top10'])
def reply_to_top_10(message):
    show_top10(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("movie:"))
def movie_from_top(call):
    bot.answer_callback_query(call.id)

    movie_id = int(call.data.split(":")[1])

    movie = search_movie_by_id(movie_id)

    send_movie_info(
        chat_id=call.message.chat.id,
        movie=movie,
        reply_markup=gen_movie_markup(movie["id"])
    )
