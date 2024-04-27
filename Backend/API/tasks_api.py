from flask import Blueprint, jsonify, request
from Models.task_model import Task

tasks_api = Blueprint('tasks_api', __name__)


@tasks_api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = [task for task in Task.select()]
    return jsonify([
        {'id': task.id, 'person': task.person, 'title': task.title,
         'description': task.description, 'status': task.status}
        for task in tasks
    ])


@tasks_api.route('/tasks', methods=['POST'])
def add_or_update_task():
    data = request.get_json()

    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    task_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if task_id:
        # Спроба знайти існуючого студента
        task = Task.get_or_none(Task.id == task_id)
        if task:
            # Оновлення існуючого студента
            task.person = data['person']
            task.title = data['title']
            task.description = data['description']
            task.status = data['status']
            task.save()
        else:
            # Якщо завдання не знайдений, створюємо нового з вказаним ID
            task = Task.create(id=task_id, **data)
    else:
        # Видалення 'id' з даних, щоб уникнути конфліктів з NULL значеннями
        data.pop('id', None)
        # Створення нового завдання без вказання ID
        task = Task.create(**data)

    return jsonify({
        'id': task.id, 'person': task.person, 'title': task.title,
        'description': task.description, 'status': task.status
    }), 200 if task_id else 201
