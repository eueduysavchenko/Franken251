from flask import Blueprint, send_from_directory, abort
import os

# Ініціалізація Blueprint для навігації браузером
students_route = Blueprint('students_route', __name__, static_folder='../../Frontend/students')


# Доступ до students.html
@students_route.route('/students')
def students_page():
    print(students_route.static_folder)
    return send_from_directory(students_route.static_folder, 'students.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@students_route.route('/students/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(students_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(students_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(students_route.static_folder, path)
