from flask import Blueprint, send_from_directory, abort
import os

# Ініціалізація Blueprint для навігації браузером
worktops_route = Blueprint('worktop_route', __name__, static_folder='../../Frontend/worktops')


# Доступ до worktops.html
@worktops_route.route('/worktops')
def worktops_page():
    # print(worktops_route.static_folder)
    return send_from_directory(worktops_route.static_folder, 'worktops.html')


# Забезпечення доступу браузера до статичних даних (image, *.js, тощо)
@worktops_route.route('/worktops/<path:path>')
def send_js(path):
    # Перевірка на недопустимі символи у шляху
    if '..' in path or path.startswith('/'):
        # Забороняємо доступ до шляху, якщо він містить небезпечні символи
        abort(404)

    # Формуємо абсолютний шлях до файлу для безпечного доступу
    safe_path = os.path.abspath(os.path.join(worktops_route.static_folder, path))

    # Перевіряємо, чи знаходиться файл дійсно у дозволеній директорії
    if not safe_path.startswith(os.path.abspath(worktops_route.static_folder)):
        abort(404)

    # Відправляємо файл за безпечним шляхом
    return send_from_directory(worktops_route.static_folder, path)