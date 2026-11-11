from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_movie_markup(movie_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопками просмотра трейлера и доступных платформ."""
    button_1 = InlineKeyboardButton(
        text="Смотреть трейлер",
        callback_data=f"trailer:{movie_id}"
    )

    button_2 = InlineKeyboardButton(
        text="Где посмотреть",
        callback_data=f"watch:{movie_id}"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2)

    return keyboard


def gen_top10_markup(movies: list[tuple[str, int]]) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора фильма из списка топ-10."""
    keyboard = InlineKeyboardMarkup()

    for title, movie_id in movies:
        button = InlineKeyboardButton(
            text=title,
            callback_data=f"movie:{movie_id}"
        )
        keyboard.add(button)

    return keyboard
