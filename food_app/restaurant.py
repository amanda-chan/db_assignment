from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Restaurants
from . import sql_db, mongo_db

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")

def retrieve_cusines():
    cuisine_types = []
    cuisines = Restaurants.query.with_entities(Restaurants.cuisine).distinct().all() # Gather all the different cuisine types
    for c in cuisines:
        # Restraunt contains more than 1 cuisine type
        if ", " in c[0]:
            temp = c[0].split(', ')
            for t in temp:
                cuisine_types.append(t)

        # Restraunt contains only than 1 cuisine type
        else:
            cuisine_types.append(c[0])
    
    cuisine_types = set(cuisine_types) # Remove duplicates
    cuisine_types = list(cuisine_types) # Convert back into a list

    return cuisine_types

def retrieve_restaurants():
    restaurant_list = []
    all_restaurants = Restaurants.query.all() # Gather all restaurants and their data

    for r in all_restaurants:
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

def filtered__restaurants(letter, cuisine, price):
    restaurant_list = []

    if letter != "":
        if cuisine != "": 
            # Letter, Cuisine & Price exists
            if price != "":
                restaurants_filtered = Restaurants.query.filter_by(price=price).filter(Restaurants.name.like(f'{letter}%'), Restaurants.cuisine.like(f'%{cuisine}%')).all()

            # Letter & Cusine exists
            else:
                restaurants_filtered = Restaurants.query.filter(Restaurants.name.like(f'{letter}%'), Restaurants.cuisine.like(f'%{cuisine}%')).all()

        else:
            # Letter & Price exists
            if price != "":
                restaurants_filtered = Restaurants.query.filter_by(price=price).filter(Restaurants.name.like(f'{letter}%')).all()

            # Only Letter Exists
            else:
                restaurants_filtered = Restaurants.query.filter(Restaurants.name.like(f'{letter}%')).all()

    else:
        if cuisine != "": 
            # Cuisine & Price exists
            if price != "":
                restaurants_filtered = Restaurants.query.filter_by(price=price).filter(Restaurants.cuisine.like(f'%{cuisine}%')).all()

            # Only Cuisine exists
            else:
                restaurants_filtered = Restaurants.query.filter(Restaurants.cuisine.like(f'%{cuisine}%')).all()
        
        else:
            # Only Price exists
            restaurants_filtered = Restaurants.query.filter_by(price=price).all()

    for r in restaurants_filtered:
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


@restaurant_bp.route("/", methods=['GET', 'POST'])
def view():

    # Gather the different cuisine types offered in the restaurant to set as a filter
    cuisine_types = retrieve_cusines()

    # Gather all the restaurants with their details
    restaurant_list = retrieve_restaurants()

    if request.method == 'POST':
        # Gather the different cuisine types offered in the restaurant to set as a filter
        cuisine_types = retrieve_cusines()

        restaurant_list = []
        letter = request.form.get("letter")
        cuisine = request.form.get("cuisine")
        price = request.form.get("price")

        # If none of the filters are applied
        if (letter == "" and cuisine == "" and price == ""):
            restaurant_list = retrieve_restaurants()

        else:
            restaurant_list = filtered__restaurants(letter, cuisine, price)

        return render_template("restaurant/view.html", cuisine_types = cuisine_types, restaurant_list = restaurant_list, user = current_user)
    
    return render_template("restaurant/view.html", cuisine_types = cuisine_types, restaurant_list = restaurant_list, user = current_user)

@restaurant_bp.route("/info")
def info():
    rid = request.args.get('rid')
    restaurant = Restaurants.query.get(rid)

    reviews = mongo_db["reviews"]

    rid_query = { "RID" : int(rid) }
    restaurant_reviews = reviews.find(rid_query)

    reviews_count = reviews.count_documents(rid_query)


    return render_template("restaurant/info.html", restaurant = restaurant, reviews = restaurant_reviews, count = reviews_count, user = current_user)
    
