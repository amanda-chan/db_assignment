from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, datetime
from .models import Customers, Orders, Restaurants
from . import sql_db, mongo_db
import re

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/")
@login_required
def profile():
    review_list = []
    booking_list = []
    order_list = []
    restaurant_list = []

    # get top 3 reviews (if available)
    reviews_col = mongo_db["reviews"]
    booking_history_col = mongo_db["bookingHistory"]

    for row in (
        reviews_col.find({"CID": current_user.get_id()})
        .limit(3)
        .sort("CreatedDateTime", -1)
    ):
        review_list.append(row)

    count = 0
    for row in booking_history_col.find({"CID": current_user.get_id()}):
        for r in row["Bookings"]:
            if count < 3 and datetime.strptime(r["Date"], "%m/%d/%Y") < datetime.now():
                print(r)
                booking_list.append(r)
                count += 1

    # get restaurant names
    if booking_list != None:
        getRestaurantNames(restaurant_list)

    return render_template(
        "profile/profile.html",
        user=current_user,
        reviews=review_list,
        bookings=booking_list,
        orders=order_list,
        restaurants=restaurant_list,
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

    getRestaurantNames(restaurant_list)

    return render_template(
        "profile/reviews.html",
        user=current_user,
        reviews=review_list,
        restaurants=restaurant_list,
    )


@profile_bp.route("/bookings")
@login_required
def bookings():
    booking_list = []
    restaurant_list = []

    booking_history_col = mongo_db["bookingHistory"]

    for row in booking_history_col.find({"CID": current_user.get_id()}):
        for r in row["Bookings"]:
            if datetime.strptime(r["Date"], "%m/%d/%Y") < datetime.now():
                print(r)
                booking_list.append(r)

    getRestaurantNames(restaurant_list)

    return render_template(
        "profile/bookings.html",
        user=current_user,
        bookings=booking_list,
        restaurants=restaurant_list,
    )


@profile_bp.route("/orders")
@login_required
def orders():
    order_list = []
    restaurant_list = []

    # get order history
    order = (
        Orders.query.filter(
            Orders.cid == current_user.get_id(), Orders.date < date.today()
        )
        .order_by(Orders.date.desc())
        .all()
    )

    for o in order:
        data = {
            "orid": o.rid,
            "date": o.date,
            "pickup_time": o.pickup_time,
            "food_items": o.food_items,
            "special_request": o.special_request,
            "rid": o.rid,
            "created_at": o.created_at,
        }
        order_list.append(data)

    getRestaurantNames(restaurant_list)

    return render_template(
        "profile/orders.html",
        user=current_user,
        orders=order_list,
        restaurants=restaurant_list,
    )


@profile_bp.route("/orders/<orid>")
@login_required
def orderDetails(orid):
    order_item = Orders()
    restaurant_list = []
    order = Orders.query.filter_by(orid=orid).all()
    for o in order:
        order_item = Orders(
            orid=o.orid,
            date=o.date,
            pickup_time=o.pickup_time,
            food_items=eval(o.food_items),
            special_request=o.special_request,
            rid=o.rid,
        )

    # Get total amount
    total = 0
    for item in eval(o.food_items):
        total += item["price"]

    getRestaurantNames(restaurant_list)

    return render_template(
        "profile/orderDetails.html",
        user=current_user,
        order=order_item,
        total=total,
        restaurants=restaurant_list,
    )


# get all restaurant names
def getRestaurantNames(restaurant_list):
    restaurant = Restaurants.query.all()
    for r in restaurant:
        data = {"rid": r.rid, "name": r.name}
        restaurant_list.append(data)
