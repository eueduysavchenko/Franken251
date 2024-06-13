from flask import Blueprint, jsonify, request
from Models.cars_model import Cars

students_api = Blueprint('cars_api', __name__)


@students_api.route('/cars', methods=['GET'])
def get_cars():
    cars = [car for car in Cars.select()]
    return jsonify([
        {'id': car.id, 'factory': car.factory, 'models_name': car.models_name,
         'country_name': car.country_name, 'engine_size': car.engine_size}
        for car in cars
    ])


@students_api.route('/cars', methods=['POST'])
def add_or_update_car():
    data = request.get_json()

    #  Перевіряємо чи переданий ID, це ключове поле яке не може бути пустим
    car_id = int(data.get('id')) if 'id' in data and data['id'] else None

    if car_id:
        # Спроба знайти існуючего авто 
        car = Cars.get_or_none(Cars.id == car_id)
        if car:
            # Оновлення існуючого авто
            car.factory = data['factory']
            car.models_name = data['models_name']
            car.country_name = data['country_name']
            car.engine_size = data['engine_size']
            car.save()
        else:
            # Якщо студент не знайдений, створюємо нового з вказаним ID
            student = Cars.create(id=car_id, **data)
    else:
        # Видалення 'id' з даних, щоб уникнути конфліктів з NULL значеннями
        data.pop('id', None)
        # Створення нового студента без вказання ID
        car = Cars.create(**data)

    return jsonify({
        'id': car.id, 'factory': car.factory, 'models_name': car.models_name,
        'country_name': car.country_name, 'engine_size': car.engine_size
    }), 200 if car_id else 201
