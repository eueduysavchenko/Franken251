from flask import Blueprint, send_from_directory, abort
import os

movies_route = Blueprint('movies_route', __name__, static_folder='../../Frontend/movies')


@movies_route.route('/movies')
def movies_page():
    print(movies_route.static_folder)
    return send_from_directory(movies_route.static_folder, 'movies.html')


@movies_route.route('/movies/<path:path>')
def send_js(path):
    if '..' in path or path.startswith('/'):
        abort(404)

    safe_path = os.path.abspath(os.path.join(movies_route.static_folder, path))

    if not safe_path.startswith(os.path.abspath(movies_route.static_folder)):
        abort(404)

    return send_from_directory(movies_route.static_folder, path)
