import os
from peewee import Model, CharField, FloatField, AutoField, SqliteDatabase

# Ініціалізація шляху до даних
# (використовуємо шлях поточного фаулй для забезпечення однакової роботи в різних середовищах)
app_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(app_dir, '../../Data', 'cars.db')
db = SqliteDatabase(db_path)


# Опис моделі
class Cars(Model):
    id = AutoField()  # Автоінкрементне первинне ключове поле
    factory = CharField()
    models_name = CharField()
    country_name = CharField()
    engine_size = FloatField()

    class Meta:
        database = db


# Створення БД та таблиць (якщо не існують)
def initialize_students_db():
    db.connect()
    db.create_tables([Cars], safe=True)
