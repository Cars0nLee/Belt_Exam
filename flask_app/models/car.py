from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Car:
    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def join(cls):
        query = "SELECT*FROM users JOIN cars ON users.id = cars.user_id"
        db_cars = connectToMySQL("users_cars").query_db(query)
        car = []
        for i in db_cars:
            user_instance = User(i)
            car_data = {
                "id": i["cars.id"],
                "price": i["price"], 
                "model": i["model"],
                "make": i["make"],
                "year": i["year"],
                "description": i["description"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"]
            }
            user_instance.carz = Car(car_data)
            car.append(user_instance)
        return car

    @classmethod
    def new_car(cls, data):
        query ="INSERT INTO cars(price, model, make, year, description, user_id) VALUES(%(price)s,%(model)s, %(make)s, %(year)s, %(description)s, %(id)s)"
        return connectToMySQL("users_cars").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE id=%(id)s"
        return connectToMySQL("users_cars").query_db(query, data)

    @classmethod
    def get_info(cls, data):
        query = "SELECT*FROM cars WHERE id=%(id)s"
        db_car = connectToMySQL("users_cars").query_db(query, data)
        return Car(db_car[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id=%(id)s"
        return connectToMySQL("users_cars").query_db(query, data)

    @classmethod
    def views(cls, data):
        query = "SELECT*FROM users JOIN cars ON users.id = cars.user_id WHERE cars.id=%(id)s"
        db_user = connectToMySQL("users_cars").query_db(query, data)
        user = User(db_user[0])
        for i in db_user:
            car_data = {
                "id": i["cars.id"],
                "price": i["price"], 
                "model": i["model"],
                "make": i["make"],
                "year": i["year"],
                "description": i["description"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"], 
                "user_id": i["user_id"]
            }
            user.cars.append(Car(car_data))
        return user


    @classmethod
    def view(cls, data):
        query = "SELECT*FROM cars WHERE id=%(id)s"
        db_car = connectToMySQL("users_cars").query_db(query, data)
        return Car(db_car[0])

    @staticmethod
    def validate(car):
        is_valid = True
        if len(car["price"]) <=0:
            flash("Price must be greater than 0", "car")
            is_valid = False
        if len(car["model"]) <= 1:
            flash("Model must be at least 1 character", "car")
            is_valid = False
        if len(car["make"]) <= 1:
            flash("Make must be at least 1 character", "car")
            is_valid = False
        if len(car["year"]) < 4:
            flash("Invalid year", "car")
            is_valid = False
        if len(car["description"]) < 10:
            flash("Description must be at least 10 characters", "car")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car["price"]) <=0:
            flash("Price must be greater than 0", "edit")
            is_valid = False
        if len(car["model"]) <= 1:
            flash("Model must be at least 1 character", "edit")
            is_valid = False
        if len(car["make"]) <= 1:
            flash("Make must be at least 1 character", "edit")
            is_valid = False
        if len(car["year"]) < 4:
            flash("Invalid year", "edit")
            is_valid = False
        if len(car["description"]) < 10:
            flash("Description must be at least 10 characters", "edit")
            is_valid = False
        return is_valid