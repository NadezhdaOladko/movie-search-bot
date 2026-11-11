from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    DateTimeField
)

db = SqliteDatabase('movies.db')


class Movie(Model):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    movie_title = CharField()
    search_date = DateTimeField()

    class Meta:
        database = db
        table_name = "movie_history"
