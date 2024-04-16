from peewee import Model, CharField, FloatField, AutoField, SqliteDatabase

# Ініціалізація шляху до даних
db = SqliteDatabase('../Data/students.db')


# Опис моделі
class Student(Model):
    id = AutoField()  # Автоінкрементне первинне ключове поле
    group = CharField()
    first_name = CharField()
    last_name = CharField()
    score = FloatField()

    class Meta:
        database = db


# Створення БД та таблиць (якщо не існують)
def initialize_students_db():
    db.connect()
    db.create_tables([Student], safe=True)
