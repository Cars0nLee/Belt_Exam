from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_validate():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"], 
            "last_name": request.form["last_name"], 
            "email": request.form["email"],
            "password": pw_hash
        }
        user_id = User.register(data)
        session["user_id"] = user_id
        flash("User Created", "register")
        return redirect("/")
    else: 
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    if User.validate_login(request.form):
        data = {
            "email": request.form["email"]
        }
        users_in_db = User.get_all_users(data)
        if not users_in_db:
            flash("Invalid Email/Password", "login")
            return redirect("/")
        if not bcrypt.check_password_hash(users_in_db.password, request.form["password"]):
            flash ("Invalid Email/Password", "login")
            return redirect("/")
        session["user_id"] = users_in_db.id
        session["first_name"] = users_in_db.first_name
        session["last_name"] = users_in_db.last_name
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out!", "login")
    return redirect("/")