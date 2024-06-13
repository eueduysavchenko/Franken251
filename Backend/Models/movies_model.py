import os
from peewee import Model, CharField, FloatField, AutoField, SqliteDatabase, IntegerField

app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, '../../Data', 'movies.db')
db = SqliteDatabase(db_path)


class Movie(Model):
    id = AutoField()
    title = CharField()
    director = CharField()
    genre = CharField()
    year_released = IntegerField()
    rating = FloatField()

    class Meta:
        database = db


def initialize_movies_db():
    db.connect()
    db.create_tables([Movie], safe=True)
