from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os

# Імпорт необхідних файлів для Students
from Models.students_model import initialize_students_db
from API.students_api import students_api as students_api
from API.students_route import students_route
# Імпорт необхідних файлів для Tasks
from Models.task_model import initialize_tasks_db
from API.tasks_api import tasks_api as tasks_api
from API.tasks_route import tasks_route
# Імпорт необхідних файлів для Library
from Models.library_model import initialize_library_db
from API.library_api import library_api as library_api
from API.library_route import library_route

# Ініціалізація app та шляху до статичних даних
app = Flask(__name__, static_folder='../Frontend')

# Дозволяє доступ до всіх доменів
CORS(app)

# Ініціалізація бази даних
initialize_students_db()
initialize_tasks_db()
initialize_library_db()

# Реєстрація Blueprints для API та Навігції FrontEnd в браузері
app.register_blueprint(students_api, url_prefix='/api')
app.register_blueprint(students_route)
app.register_blueprint(tasks_api, url_prefix='/api')
app.register_blueprint(tasks_route)
app.register_blueprint(library_api, url_prefix='/api')
app.register_blueprint(library_route)


# Точка входу, index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@app.route('/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    if path.startswith('/students'):
        # Формуємо абсолютний шлях до файлу для безпечного доступу
        safe_path = os.path.abspath(os.path.join(students_route.static_folder, path))
        # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
        if not safe_path.startswith(os.path.abspath(students_route.static_folder)):
            abort(404)
        # Відправляємо файл за безпечним шляхом
        return send_from_directory(students_route.static_folder, path)

    if path.startswith('/tasks'):
        # Формуємо абсолютний шлях до файлу для безпечного доступу
        safe_path = os.path.abspath(os.path.join(tasks_route.static_folder, path))
        # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
        if not safe_path.startswith(os.path.abspath(tasks_route.static_folder)):
            abort(404)
        # Відправляємо файл за безпечним шляхом
        return send_from_directory(tasks_route.static_folder, path)

    if path.startswith('/library'):
        # Формуємо абсолютний шлях до файлу для безпечного доступу
        safe_path = os.path.abspath(os.path.join(library_route.static_folder, path))
        # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
        if not safe_path.startswith(os.path.abspath(library_route.static_folder)):
            abort(404)
        # Відправляємо файл за безпечним шляхом
        return send_from_directory(library_route.static_folder, path)

# Запуск сервера в режимі тестування
if __name__ == '__main__':
    app.run(debug=True, port=8080)


# MykhailoZhuravel_api