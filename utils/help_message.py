from loader import bot
from keyboards.main_menu import gen_help_menu_markup


def show_help(chat_id: int) -> None:
    """Отправляет сообщение пользователю со списком доступных команд."""
    text = ("📚 Доступные команды\n\n"
            "/start — запуск бота\n"
            "/help — справка\n"
            "/movie — найти фильм по названию\n"
            "/random — случайный фильм\n"
            "/top10 — лучшие фильмы по версии TMDb\n"
            "/history — история ваших запросов\n\n"
            "Вы можете ввести команды с клавиатуры, либо выбрать доступное действие ⬇️."
            )
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=gen_help_menu_markup()
    )