from telebot.types import ReplyKeyboardRemove

from loader import bot


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "🎬 Добро пожаловать в Movie Search Bot!\n\n"
        "Я помогу найти информацию о фильмах, показать топ-10 лучших картин "
        "и подобрать случайный фильм для просмотра.\n\n"
        "Чтобы посмотреть список всех команд, используйте команду /help "
        "или нажмите «Меню» слева от строки ввода."
    )