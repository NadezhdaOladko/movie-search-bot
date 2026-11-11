from loader import bot
from keyboards.main_menu import gen_main_menu_markup
from utils.help_message import show_help


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "🎬 Добро пожаловать в Movie Search Bot!\n\n"
        "Я помогу найти информацию о фильмах, показать топ-10 лучших картин "
        "и подобрать случайный фильм для просмотра.\n\n"
        "Чтобы посмотреть список всех команд, используйте команду /help или нажмите главное меню.",
        reply_markup=gen_main_menu_markup()
    )


@bot.message_handler(func=lambda message: message.text == "Главное меню")
def handle_main_menu_button(message):
    show_help(message.chat.id)