import os
from peewee import Model, CharField, AutoField, BooleanField, SqliteDatabase

# Ініціалізація шляху до даних
# (використовуємо шлях поточного фаулй для забезпечення однакової роботи в різних середовищах)
app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, '../../Data', 'library.db')
db = SqliteDatabase(db_path)


# Опис моделі
class Library(Model):
    id = AutoField()  # Автоінкрементне первинне ключове поле
    title = CharField()
    author = CharField()
    taken = BooleanField(default=False)

    class Meta:
        database = db


# Створення БД та таблиць (якщо не існують)
def initialize_library_db():
    db.connect()
    db.create_tables([Library], safe=True)
