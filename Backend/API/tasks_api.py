from flask import Blueprint, jsonify, request
from Models.task_model import Task

tasks_api = Blueprint('tasks_api', __name__)


@tasks_api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = [task for task in Task.select()]
    return jsonify([{
        'id': task.id,
        'person': task.person,
        'title': task.title,
        'description': task.description,
        'status': task.status
    }
        for task in tasks
    ])

@tasks_api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.get_by_id(task_id)
        return jsonify({
            'id': task.id,
            'person': task.person,
            'title': task.title,
            'description': task.description,
            'status': task.status
        })
    except Task.DoesNotExist:
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tasks_api.route('/tasks', methods=['POST'])
def add_task():
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

@tasks_api.route('/tasks/delete-task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.get(Task.id == task_id)
        task.delete_instance()
        return jsonify({'success': True, 'message': 'Task deleted successfully'})
    except Task.DoesNotExist:
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_api.route('/tasks/update-task/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    try:
        data = request.get_json()
        task = Task.get(Task.id == task_id)
        task.person = data.get('person', task.person)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)

        task.save()
        return jsonify({'success': True, 'message': 'Task updated successfully'})
    except Task.DoesNotExist:
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500