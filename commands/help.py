from loader import bot
from utils.help_message import show_help
from commands.movie import start_movie_search
from commands.random import send_random_movie_impl
from commands.top10 import show_top10
from commands.history import show_history


@bot.message_handler(commands=['help'])
def send_help(message):
    show_help(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "menu_movie")
def menu_movie_handler(call):
    bot.answer_callback_query(call.id)

    start_movie_search(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "menu_random")
def menu_random_handler(call):
    bot.answer_callback_query(call.id)
    send_random_movie_impl(call.message.chat.id, call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == "menu_top10")
def menu_top10_handler(call):
    bot.answer_callback_query(call.id)
    show_top10(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "menu_history")
def menu_history_handler(call):
    bot.answer_callback_query(call.id)
    show_history(call.message.chat.id, call.from_user.id)