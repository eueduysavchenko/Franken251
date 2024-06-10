from flask import Blueprint, jsonify, request
from Models.library_model import Library

library_api = Blueprint('library_api', __name__)


@library_api.route('/library', methods=['GET'])
def get_books():
    books = [book for book in Library.select()]
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'taken': book.taken
    }
        for book in books
    ])

@library_api.route('/library', methods=['POST'])
def add_book():
    data = request.get_json()
    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    author = data.get('author') if 'author' in data and data['author'] else None
    title = data.get('title') if 'title' in data and data['title'] else None

    if author and title:
        book = Library.create(author=author, title=title, taken=False)
        return jsonify({
            'id': book.id,
            'author': book.author,
            'title': book.title,
            'taken': book.taken
        }), 200
    else:
        return jsonify({'error': 'Title or author is missing!'}), 404
