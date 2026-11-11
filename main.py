import commands.start
import commands.help
import commands.movie
import commands.random
import commands.top10
import commands.history
from database.database import Movie, db
from loader import bot
from telebot.custom_filters import StateFilter

bot.add_custom_filter(StateFilter(bot))


if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    db.create_tables([Movie])
    try:
        bot.infinity_polling()
    finally:
        db.close()
