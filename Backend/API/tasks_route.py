from flask import Blueprint, send_from_directory, abort
import os

# Ініціалізація Blueprint для навігації браузером
tasks_route = Blueprint('tasks_route', __name__, static_folder='../../Frontend/tasks')


# Доступ до tasks.html
@tasks_route.route('/tasks')
def tasks_page():
    print(tasks_route.static_folder)
    return send_from_directory(tasks_route.static_folder, 'tasks.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@tasks_route.route('/tasks/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(tasks_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(tasks_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(tasks_route.static_folder, path)
