from flask import Flask, send_from_directory
from flask_cors import CORS

# Імпорт необхідних файлів для Students
from Backend.Models.students_model import initialize_students_db
from API.students_api import students_api as students_api
from API.students_route import students_route

# Ініціалізація app та шляху до статичних даних
app = Flask(__name__, static_folder='../Frontend')

# Дозволяє доступ до всіх доменів
CORS(app)

# Ініціалізація бази даних
initialize_students_db()

# Реєстрація Blueprints для API та Навігції FrontEnd в браузері
app.register_blueprint(students_api, url_prefix='/api')
app.register_blueprint(students_route)


# Точка входу, index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder, path)


# Запуск сервера в режимі тестування
if __name__ == '__main__':
    app.run(debug=True, port=8080)
