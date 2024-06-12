from flask import Blueprint, jsonify, request

from Backend.Models.teachers_model import Teacher

teachers_api = Blueprint('teachers_api', __name__)


@teachers_api.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = [teacher for teacher in Teacher.select()]
    return jsonify([
        {'id': teacher.id, 'group': teacher.group, 'first_name': teacher.first_name,
         'last_name': teacher.last_name}
        for teacher in teachers
    ])


@teachers_api.route('/teachers', methods=['POST'])
def add_or_update_teacher():
    data = request.get_json()

    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    teacher_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if teacher_id:
        # Спроба знайти існуючого вчителя
        teacher = Teacher.get_or_none(Teacher.id == teacher_id)
        if teacher:
            # Оновлення існуючого вчителя
            teacher.group = data['group']
            teacher.first_name = data['first_name']
            teacher.last_name = data['last_name']
            teacher.save()
        else:
            # Якщо вчитель не знайдений, створюємо нового з вказаним ID
            teacher = teacher.create(id=teacher_id, **data)
    else:
        # Видалення 'id' з даних, щоб уникнути конфліктів з NULL значеннями
        data.pop('id', None)
        # Створення нового вчителя без вказання ID
        teacher = Teacher.create(**data)

    return jsonify({
        'id': teacher.id, 'group': teacher.group, 'first_name': teacher.first_name,
        'last_name': teacher.last_name
    }), 200 if teacher_id else 201
