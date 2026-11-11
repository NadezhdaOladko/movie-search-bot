from loader import bot


def send_movie_info(chat_id: int, movie: dict, reply_markup=None) -> None:
    """Отправляет информацию о фильме пользователю."""
    text = (
        f"🎬 {movie['title']}\n\n"
        f"⭐ Рейтинг: {movie['rating']}\n"
        f"📅 Дата выхода: {movie['release_date']}\n\n"
        f"📝 {movie['overview']}"
    )
    if movie["poster"]:
        bot.send_photo(
            chat_id=chat_id,
            photo=movie["poster"]
        )

    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )