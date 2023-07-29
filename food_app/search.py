from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from .models import Restaurants
from . import mongo_db

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("/", methods=["GET", "POST"])
def search():
    restaurant_list = []
    message = ""
    results = 0

    if request.method == "POST":
        keyword = request.form.get("keyword")

        results = Restaurants.query.filter(Restaurants.name.like(f"%{keyword}%")).count()

        if keyword != "":
            restaurants_search = Restaurants.query.filter(
                Restaurants.name.like(f"%{keyword}%")
            ).all()

            for r in restaurants_search:
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

            if results == 0:
                message = 'No restaurant with name "' + keyword + '" found.'

    return render_template(
        "search/index.html",
        user=current_user,
        restaurants=restaurant_list,
        message=message,
        results=results
    )
