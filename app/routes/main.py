from flask import Blueprint, render_template
from app.models.food_item import FoodItem

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    food_items = FoodItem.query.all()
    return render_template("home.html", food_items=food_items)

@main.route("/about")
def about():
    return render_template("about.html", title="About")

