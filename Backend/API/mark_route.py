import os
from flask import Blueprint, send_from_directory, abort

# Ініціалізація Blueprint для навігації браузером
mark_route = Blueprint('note_route', __name__, static_folder='../../Frontend/mark')


# Доступ до notes.html
@mark_route.route('/mark')
def notes_page():
    print(mark_route.static_folder)
    return send_from_directory(mark_route.static_folder, 'notes.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@mark_route.route('/mark/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(mark_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(mark_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(mark_route.static_folder, path)