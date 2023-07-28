from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Customers, Bookings, Orders, Restaurants
from . import sql_db, mongo_db
import re

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/")
@login_required
def profile():
    r_list = []
    b_list = []
    o_list = []

    reviews_col = mongo_db["reviews"]

    if len(list(reviews_col.find({"CID": current_user.get_id()}))) <= 3:
        for row in reviews_col.find({"CID": current_user.get_id()}).sort("CreatedDateTime", -1):
            r_list.append(row)
    else:
        for row in reviews_col.find({"CID": current_user.get_id()}).limit(3).sort("CreatedDateTime", -1):
            r_list.append(row)

    return render_template(
        "profile/profile.html",
        user=current_user,
        reviews=r_list,
        bookings=b_list,
        orders=o_list,
    )


@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        contact_number = request.form.get("contact-number")

        customer = sql_db.session.query(Customers).get(current_user.get_id())
        if len(email) < 3:
            flash("Email must be at least 3 characters.", category="error")
        elif len(username) < 3:
            flash("First name must be at least 3 character.", category="error")
        elif re.search("^[89][0-9]{7}$", str(contact_number)) is None:
            flash("Please enter a valid local phone number.", category="error")
        else:
            customer.email = email
            customer.username = username
            customer.contact_number = contact_number
            customer.updated_at = datetime.now()
            sql_db.session.commit()
            return redirect(url_for("profile.profile"))
    return render_template("profile/edit.html", user=current_user)


@profile_bp.route("/reviews")
@login_required
def reviews():
    review_list = []
    restaurant_list = []

    # Get reviews collections from the db
    reviews_col = mongo_db["reviews"]

    # Gather reviews by current user
    query = reviews_col.find({"CID": current_user.get_id()}).sort("CreatedDateTime", -1)

    for row in query:
        review_list.append(row)
        restaurant = Restaurants.query.filter_by(rid=row["RID"]).all()
        for r in restaurant:
            data = {"rid": r.rid, "name": r.name}
            restaurant_list.append(data)

    return render_template(
        "profile/reviews.html",
        user=current_user,
        reviews=review_list,
        restaurants=restaurant_list,
    )


@profile_bp.route("/bookings")
def bookings():
    # add login required ^
    return render_template(
        "profile/bookings.html", user=current_user, bookings=bookings
    )


@profile_bp.route("/orders")
def orders():
    # add login required ^
    return render_template("profile/orders.html", user=current_user, orders=orders)
