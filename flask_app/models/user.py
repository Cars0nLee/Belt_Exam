from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.cars = []

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("users_cars").query_db(query, data)
    
    @classmethod
    def get_all_users(cls, data):
        query = "SELECT*FROM users WHERE email = %(email)s"
        user_db = connectToMySQL("users_cars").query_db(query, data)
        if len(user_db) < 1:
            return False
        return User(user_db[0])


    @staticmethod
    def validate_user(user):
        email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
        name_regex = re.compile(r'^[a-zA-Z ]+$')
        is_valid = True
        if len(user["first_name"]) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid = False
        if not name_regex.match(user["first_name"]):
            flash("Letters only for first name", "register")
            is_valid = False
        if not name_regex.match(user["last_name"]):
            flash("Letters only for last name", "register")
            is_valid = False
        if not email_regex.match(user["email"]):
            flash("Invalid Email", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if (user["password"] != user["confirm_password"]):
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user["email"]) < 3:
            flash("Invalid Email/Password", "login")
            is_valid = False
        return is_valid