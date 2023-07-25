from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Restaurant
from . import sql_db

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")


@restaurant_bp.route("/", methods=['GET', 'POST'])
def view():

    # Gather the different cuisine types offered in the restaurant to set as a filter
    cuisine_types = []
    cuisines = Restaurant.query.with_entities(Restaurant.cuisine).distinct().all() # Gather all the different cuisine types
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

    if request.method == 'POST':
        return render_template("restaurant/view.html")
    
    return render_template("restaurant/view.html", cuisine_types = cuisine_types)


@restaurant_bp.route("/edit", methods=["GET", "POST"])
def edit():
    # add login required ^
    return render_template("profile/edit.html", user=current_user)

