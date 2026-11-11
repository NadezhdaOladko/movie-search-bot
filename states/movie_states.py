from telebot.handler_backends import State, StatesGroup


class MovieStates(StatesGroup):
    waiting_movie_name = State()