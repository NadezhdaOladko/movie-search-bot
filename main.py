import commands.start
import commands.help
import commands.movie
import commands.random
import commands.top10
import commands.history
from database.database import Base, engine
from loader import bot
from telebot.custom_filters import StateFilter

bot.add_custom_filter(StateFilter(bot))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    bot.infinity_polling()
