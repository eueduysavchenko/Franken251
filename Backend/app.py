from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os

# Імпорт необхідних файлів для teachers
from Models.teachers_model import initialize_teachers_db
from API.teachers_api import teachers_api
from API.teachers_route import teachers_route

# Ініціалізація app та шляху до статичних даних
app = Flask(__name__, static_folder='../Frontend')

# Дозволяє доступ до всіх доменів
CORS(app)

# Ініціалізація бази даних
initialize_teachers_db()

# Реєстрація Blueprints для API та Навігції FrontEnd в браузері
app.register_blueprint(teachers_api, url_prefix='/api')
app.register_blueprint(teachers_route)


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

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(teachers_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(teachers_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(teachers_route.static_folder, path)


# Запуск сервера в режимі тестування
if __name__ == '__main__':
    app.run(debug=True, port=8082)
