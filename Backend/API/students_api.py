from flask import Blueprint, jsonify, request
from Backend.Models.students_model import Student

students_api = Blueprint('students_api', __name__)


@students_api.route('/students', methods=['GET'])
def get_students():
    students = [student for student in Student.select()]
    return jsonify([
        {'id': student.id, 'group': student.group, 'first_name': student.first_name,
         'last_name': student.last_name, 'score': student.score}
        for student in students
    ])


@students_api.route('/students', methods=['POST'])
def add_or_update_student():
    data = request.get_json()

    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    student_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if student_id:
        # Спроба знайти існуючого студента
        student = Student.get_or_none(Student.id == student_id)
        if student:
            # Оновлення існуючого студента
            student.group = data['group']
            student.first_name = data['first_name']
            student.last_name = data['last_name']
            student.score = data['score']
            student.save()
        else:
            # Якщо студент не знайдений, створюємо нового з вказаним ID
            student = Student.create(id=student_id, **data)
    else:
        # Видалення 'id' з даних, щоб уникнути конфліктів з NULL значеннями
        data.pop('id', None)
        # Створення нового студента без вказання ID
        student = Student.create(**data)

    return jsonify({
        'id': student.id, 'group': student.group, 'first_name': student.first_name,
        'last_name': student.last_name, 'score': student.score
    }), 200 if student_id else 201
