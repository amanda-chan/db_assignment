from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from .models import Restaurants
from . import mongo_db

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@home_bp.route("/home")
def home():
    restaurant_list = []
    average_rating_list = []

    reviews_col = mongo_db["reviews"]
    query = reviews_col.aggregate(
        [
            {"$group": {"_id": "$RID", "avgRating": {"$avg": "$Rating"}}},
            {"$sort": {"avgRating": -1}},
            {"$limit": 10},
        ]
    )

    for row in query:
        print(row)
        average_rating_list.append(row)
        restaurant = Restaurants.query.filter_by(
            rid=row["_id"]
        ).all()  # Gather all restaurants and their data

        for r in restaurant:
            data = {
                "rid": r.rid,
                "name": r.name,
                "cuisine": r.cuisine,
                "operating_hours": r.operating_hours,
                "operating_days": r.operating_days,
                "address": r.address,
                "contact_number": r.contact_number,
                "email": r.email,
                "price": r.price,
            }
            restaurant_list.append(data)

    return render_template(
        "home/index.html",
        user=current_user,
        restaurants=restaurant_list,
        average_rating=average_rating_list,
    )
