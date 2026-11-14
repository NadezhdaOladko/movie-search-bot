import commands.start
import commands.help
import commands.movie
import commands.random
import commands.top10
import commands.history

from database.database import Base, engine
from loader import bot
from telebot.types import BotCommand, MenuButtonCommands
from telebot.custom_filters import StateFilter


bot.add_custom_filter(StateFilter(bot))


def setup_bot_menu():
    bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("help", "Помощь"),
        BotCommand("movie", "Найти фильм"),
        BotCommand("random", "Случайный фильм"),
        BotCommand("top10", "Топ-10 фильмов"),
        BotCommand("history", "История поиска"),
    ])

    bot.set_chat_menu_button(
        menu_button=MenuButtonCommands()
    )


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    setup_bot_menu()
    bot.infinity_polling()
