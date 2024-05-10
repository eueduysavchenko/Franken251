# https://docs.peewee-orm.com/en/latest/peewee/querying.html#deleting-records

from flask import Blueprint, jsonify, request
from Models.mark_model import Note

note_api = Blueprint('note_api', __name__)


@note_api.route('/mark', methods=['GET'])
def get_notes():
    notes = [n for n in Note.select()]
    return jsonify([
        {'id': n.id, 'name': n.name, 'task': n.task,
         'status': n.status, 'date_time': n.date_time}
        for n in notes
    ])


@note_api.route('/mark', methods=['POST'])
def add_or_update_note():
    data = request.get_json()
    print(data)

    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    note_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if note_id:
        # Спроба знайти існуючий запис
        note = Note.get_or_none(Note.id == note_id)
        if note:
            # Оновлення існуючих записів
            note.name = data['name']
            note.task = data['task']
            note.status = data['status']
            note.date_time = data['date_time']
            note.save()
        else:
            # Якщо запису не знайдено, створюємо новий з вказаним ID
            note = Note.create(id=note_id, **data)
    else:
        # Видалення 'id' з даних, щоб уникнути конфліктів з NULL значеннями
        data.pop('id', None)
        # Створення нового запису без вказання ID
        note = Note.create(**data)

    return jsonify({
        'id': note.id, 'name': note.name, 'task': note.task,
        'status': note.status, 'date_time': note.date_time
    }), 200 if note_id else 201


@note_api.route('/mark/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    print(note_id)
    try:
        note = Note.get(note_id)
        print(note)
        note.delete_instance()
        return jsonify({'message': 'Record deleted successfully'}), 200
    except Note.DoesNotExist:
        return jsonify({'message': 'Record does not exist'}), 404
    except Exception as e:
        return jsonify({'message': e}), 500