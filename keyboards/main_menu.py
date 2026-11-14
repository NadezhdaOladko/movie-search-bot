from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def gen_help_menu_markup() -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру с основными действиями бота."""
    button_1 = InlineKeyboardButton(
        text="Найти фильм по названию",
        callback_data="menu_movie"
    )
    button_2 = InlineKeyboardButton(
        text="Случайный фильм",
        callback_data="menu_random"
    )
    button_3 = InlineKeyboardButton(
        text="Топ 10 лучших фильмов",
        callback_data="menu_top10"
    )
    button_4 = InlineKeyboardButton(
        text="История запросов",
        callback_data="menu_history"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3, button_4)

    return keyboard

