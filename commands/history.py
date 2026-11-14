from sqlalchemy import select, delete

from loader import bot
from database.database import Movie, Session
from keyboards.history_keyboard import gen_history_markup


def show_history(chat_id: int, user_id: int) -> None:
    """Отправляет пользователю последние 10 записей истории поиска фильмов."""

    with Session() as session:
        history = session.scalars(
            select(Movie)
            .where(Movie.user_id == user_id)
            .order_by(Movie.id.desc())
            .limit(10)
        ).all()

    if not history:
        bot.send_message(
            chat_id,
            "📚 История запросов пока пуста.\n"
            "Используйте /movie или /random, чтобы найти фильм."
        )
        return

    text = "📚 Последние 10 запросов\n\n"

    for count, movie in enumerate(history, start=1):
        text += (
            f"{count}. {movie.movie_title}\n"
            f"🕒 {movie.search_date.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        )

    bot.send_message(
        chat_id,
        text,
        reply_markup=gen_history_markup()
    )


@bot.message_handler(commands=["history"])
def send_history(message):
    show_history(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == "del_history")
def handle_del_history_callback(call):
    with Session() as session:
        session.execute(delete(Movie).where(Movie.user_id == call.from_user.id))
        session.commit()

    bot.answer_callback_query(call.id, "История удалена")
    bot.edit_message_text(
        "📚 История запросов очищена.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )