import re
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.car import Car


@app.route("/dashboard")
def dash():
    if "user_id" not in session:
        flash("Must be logged in to view page", "login")
        return redirect("/")
    else:
        x = Car.join()
        return render_template("dashboard.html", car=x)

@app.route("/add_car")
def add_car():
    if "user_id" not in session:
        flash("Must be logged in to view page", "login")
        return redirect("/")
    else:
        return render_template("forsale.html")

@app.route("/add", methods=["POST"])
def add():
    if Car.validate(request.form):
        data = {
            "price": request.form["price"],
            "model": request.form["model"],
            "make": request.form["make"], 
            "year": request.form["year"],
            "description": request.form["description"],
            "id": session["user_id"]
        }
        Car.new_car(data)
        flash("New Car Listed!!!", "dash")
        return redirect("/dashboard")
    else:
        return redirect("/add_car")

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session:
        flash("Must be logged in to view page", "login")
        return redirect("/")
    else:
        data = {
        "id": id
        }
        x = Car.get_info(data)
        return render_template("edit.html", edit=x)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if Car.validate_car(request.form):
        data ={
            "id": id,
            "price": request.form["price"],
            "model": request.form["model"],
            "make": request.form["make"],
            "year": request.form["year"],
            "description": request.form["description"]
        }
        Car.update(data)
        flash("Updated!", "dash")
        return redirect("/dashboard")
    else:
        return redirect("/edit/"+str(id))

@app.route("/view/<int:id>")
def view(id):
    if "user_id" not in session:
        flash("Must be logged in to view page", "login")
        return redirect("/")
    else:
        data = {
        "id": id
        }
        x = Car.view(data)
        y =Car.views(data)
        return render_template("view.html", view=x, owner=y)

@app.route("/purchase/<int:id>")
def purchase(id):
    data={
        "id": id
    }
    Car.delete(data)
    flash("Vehicle Purchased!!!", "dash")
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    data = {
        "id": id
    }
    Car.delete(data)
    flash("Deleted!", "dash")
    return redirect("/dashboard")
