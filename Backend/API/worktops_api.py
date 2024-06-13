from flask import Blueprint, jsonify, request
from Models.worktop_model import Worktop

worktop_api = Blueprint('worktop_api', __name__)


@worktop_api.route('/worktops', methods=['GET'])
def get_worktops():
    worktops = [worktop for worktop in Worktop.select()]
    return jsonify([{
        'id': worktop.id,
        'person': worktop.person,
        'title': worktop.title,
        'description': worktop.description,
        'status': worktop.status
    }
        for worktop in worktops
    ])


@worktop_api.route('/worktops/<int:worktop_id>', methods=['GET'])
def get_worktop(worktop_id):
    try:
        worktop = Worktop.get_by_id(worktop_id)
        return jsonify({
            'id': worktop.id,
            'person': worktop.person,
            'title': worktop.title,
            'description': worktop.description,
            'status': worktop.status
        })
    except Worktop.DoesNotExist:
        return jsonify({'success': False, 'message': 'Worktop not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@worktop_api.route('/worktops', methods=['POST'])
def add_worktop():
    data = request.get_json()
    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    worktop_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if worktop_id:
        # Спроба знайти існуючого студента
        worktop = Worktop.get_or_none(Worktop.id == worktop_id)
        if worktop:
            # Оновлення існуючого студента
            worktop.person = data['person']
            worktop.title = data['title']
            worktop.description = data['description']
            worktop.status = data['status']
            worktop.save()
        else:
            # Якщо завдання не знайдений, створюємо нового з вказаним ID
            worktop = Worktop.create(id=worktop_id, **data)
    else:
        # Видалення 'id' з даних, щоб уникнути конфліктів з NULL значеннями
        data.pop('id', None)
        # Створення нового завдання без вказання ID
        worktop = Worktop.create(**data)

    return jsonify({
        'id': worktop.id, 'person': worktop.person, 'title': worktop.title,
        'description': worktop.description, 'status': worktop.status
    }), 200 if worktop_id else 201


@worktop_api.route('/worktops/<worktop_id>', methods=['DELETE'])
def delete_worktop(worktop_id):
    try:
        worktop = Worktop.get(Worktop.id == worktop_id)
        worktop.delete_instance()
        return jsonify({'success': True, 'message': 'Worktop deleted successfully'})
    except Worktop.DoesNotExist:
        return jsonify({'success': False, 'message': 'Worktop not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@worktop_api.route('/worktops/<int:worktop_id>', methods=['PATCH'])
def update_worktop(worktop_id):
    try:
        data = request.get_json()
        worktop = Worktop.get(Worktop.id == worktop_id)
        worktop.person = data.get('person', worktop.person)
        worktop.title = data.get('title', worktop.title)
        worktop.description = data.get('description', worktop.description)
        worktop.status = data.get('status', worktop.status)

        worktop.save()
        return jsonify({'success': True, 'message': 'Worktop updated successfully'})
    except Worktop.DoesNotExist:
        return jsonify({'success': False, 'message': 'Worktop not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
