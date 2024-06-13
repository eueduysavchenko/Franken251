from flask import Blueprint, jsonify, request
from Models.movies_model import Movie

movies_api = Blueprint('movies_api', __name__)


@movies_api.route('/movies', methods=['GET'])
def get_movies():
    movies = [movie for movie in Movie.select()]
    return jsonify([
        {'id': movie.id, 'title': movie.title, 'director': movie.director,
         'genre': movie.genre, 'year_released': movie.year_released, 'rating': movie.rating}
        for movie in movies
    ])


@movies_api.route('/movies', methods=['POST'])
def add_or_update_movie():
    data = request.get_json()

    movie_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if movie_id:
        movie = Movie.get_or_none(Movie.id == movie_id)
        if movie:
            movie.title = data['title']
            movie.director = data['director']
            movie.genre = data['genre']
            movie.year_released = data['year_released']
            movie.rating = data['rating']
            movie.save()
        else:
            movie = Movie.create(id=movie_id, **data)
    else:
        data.pop('id', None)
        movie = Movie.create(**data)

    return jsonify({
        'id': movie.id, 'title': movie.title, 'director': movie.director,
        'genre': movie.genre, 'year_released': movie.year_released, 'rating': movie.rating
    }), 200 if movie_id else 201


# My code
@movies_api.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.get_or_none(Movie.id == movie_id)
    if movie:
        movie.delete_instance()
        return jsonify({'message': 'Movie deleted successfully'}), 200
    return jsonify({'message': 'Movie not found'}), 404

