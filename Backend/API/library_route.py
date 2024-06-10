from flask import Blueprint, send_from_directory, abort
import os

# Ініціалізація Blueprint для навігації браузером
library_route = Blueprint('library_route', __name__, static_folder='../../Frontend/library')


# Доступ до library.html
@library_route.route('/library')
def library_page():
    print(library_route.static_folder)
    return send_from_directory(library_route.static_folder, 'library.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@library_route.route('/library/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(library_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(library_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(library_route.static_folder, path)
