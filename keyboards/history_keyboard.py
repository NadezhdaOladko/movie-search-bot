from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_history_markup() -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру с кнопкой очистки истории поиска."""
    keyboard = InlineKeyboardMarkup()

    button = InlineKeyboardButton(
        text="Удалить историю",
        callback_data="del_history"
    )

    keyboard.add(button)

    return keyboard