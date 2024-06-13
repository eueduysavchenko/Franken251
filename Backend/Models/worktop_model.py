import os
from peewee import Model, CharField, AutoField, SqliteDatabase

# Ініціалізація шляху до даних
# (використовуємо шлях поточного фаулй для забезпечення однакової роботи в різних середовищах)
app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, '../../Data', 'worktops.db')
db = SqliteDatabase(db_path)


# Опис моделі
class Worktop(Model):
    id = AutoField()  # Автоінкрементне первинне ключове поле
    person = CharField()
    title = CharField()
    description = CharField()
    status = CharField()

    class Meta:
        database = db


# Створення БД та таблиць (якщо не існують)
def initialize_worktops_db():
    db.connect()
    db.create_tables([Worktop], safe=True)
