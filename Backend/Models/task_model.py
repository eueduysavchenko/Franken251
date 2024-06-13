import os
from peewee import Model, CharField, AutoField, SqliteDatabase

# Ініціалізація шляху до даних
# (використовуємо шлях поточного фаулй для забезпечення однакової роботи в різних середовищах)
app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, '../../Data', 'tasks.db')
db = SqliteDatabase(db_path)


# Опис моделі
class Task(Model):
    id = AutoField()  # Автоінкрементне первинне ключове поле
    person = CharField()
    title = CharField()
    description = CharField()
    status = CharField()

    class Meta:
        database = db


# Створення БД та таблиць (якщо не існують)
def initialize_tasks_db():
    db.connect()
    db.create_tables([Task], safe=True)
