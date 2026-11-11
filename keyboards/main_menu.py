from telebot.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )


def gen_main_menu_markup() -> ReplyKeyboardMarkup:
    """Создает постоянную клавиатуру с кнопкой перехода в главное меню."""
    button = KeyboardButton(text="Главное меню")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button)

    return keyboard


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

