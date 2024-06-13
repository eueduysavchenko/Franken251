import os
from peewee import Model, CharField, AutoField, SqliteDatabase

# Ініціалізація шляху до даних
# (використовуємо шлях поточного фаулй для забезпечення однакової роботи в різних середовищах)
app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, '../../Data', 'teacher.db')
db = SqliteDatabase(db_path)


# Опис моделі
class Teacher(Model):
    id = AutoField()  # Автоінкрементне первинне ключове поле
    group = CharField()
    first_name = CharField()
    last_name = CharField()


    class Meta:
        database = db


# Створення БД та таблиць (якщо не існують)
def initialize_teachers_db():
    db.connect()
    db.create_tables([Teacher], safe=True)
