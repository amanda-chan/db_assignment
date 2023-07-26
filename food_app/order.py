from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Restaurants
from . import sql_db, mongo_db

order_bp = Blueprint("order", __name__, url_prefix="/order")

def get_restaurants():
    restaurant_list = []

    # Get menu collections from the db
    menu = mongo_db["menu"]

    # Gather distinct rids
    rid_list = menu.distinct("RID")

    # Gather restaurant found in rid_list
    for rid in rid_list:
        restaurant = Restaurants.query.filter_by(rid=rid).all()
        for r in restaurant: # Since data returned is in a list
            data = {
                'rid': r.rid,
                'name': r.name,
                'cuisine': r.cuisine,
                'operating_hours': r.operating_hours,
                'operating_days': r.operating_days,
                'address': r.address,
                'contact_number': r.contact_number,
                'email': r.email,
                'price': r.price
            }
            
            restaurant_list.append(data)

    return restaurant_list


@order_bp.route("/")
def view():

    # Gather restaurants thats only can be ordered from
    restaurant_list = get_restaurants()

    return render_template("order/view.html", restaurant_list = restaurant_list, user = current_user)