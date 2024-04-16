from flask import Blueprint, send_from_directory

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
    return send_from_directory(students_route.static_folder, path)
