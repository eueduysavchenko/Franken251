from flask import Blueprint, send_from_directory, abort
import os

# Ініціалізація Blueprint для навігації браузером
teachers_route = Blueprint('teachers_route', __name__, static_folder='../../Frontend/teachers')


# Доступ до teachers.html
@teachers_route.route('/teachers')
def teachers_page():
    print(teachers_route.static_folder)
    return send_from_directory(teachers_route.static_folder, 'teachers.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@teachers_route.route('/teachers/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(teachers_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(teachers_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(teachers_route.static_folder, path)
