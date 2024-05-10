from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os

# Імпорт необхідних файлів для Students
from Models.students_model import initialize_students_db
from API.students_api import students_api as students_api
from API.students_route import students_route
# Імпорт необхвдного для Mark
from Models.mark_model import initialize_mark_db
from API.mark_api import note_api
from API.mark_route import mark_route

# Ініціалізація app та шляху до статичних даних
app = Flask(__name__, static_folder='../Frontend')

# Дозволяє доступ до всіх доменів
CORS(app)

# Ініціалізація бази даних
initialize_students_db()
# Ініціалізація бази даних для Note(Mark)
initialize_mark_db()

# Реєстрація Blueprints для API та Навігції FrontEnd в браузері
app.register_blueprint(students_api, url_prefix='/api')
app.register_blueprint(students_route)
# Реєстрація Blueprints для API та Навігції FrontEnd в браузері
app.register_blueprint(note_api, url_prefix='/api')
app.register_blueprint(mark_route)

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

    if path.startswith('/mark'):
        # Формуємо абсолютний шлях до файлу для безпечного доступу
        safe_path = os.path.abspath(os.path.join(mark_route.static_folder, path))

        # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
        if not safe_path.startswith(os.path.abspath(mark_route.static_folder)):
            abort(404)

        # Відправляємо файл за безпечним шляхом
        return send_from_directory(mark_route.static_folder, path)

# Запуск сервера в режимі тестування
if __name__ == '__main__':
    app.run(debug=True, port=8080)
