from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, datetime, time
from .models import Customers, Bookings, Orders, Restaurants
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

    if len(list(reviews_col.find({"CID": current_user.get_id()}))) <= 3:
        for row in reviews_col.find({"CID": current_user.get_id()}).sort(
            "CreatedDateTime", -1
        ):
            review_list.append(row)
    else:
        for row in (
            reviews_col.find({"CID": current_user.get_id()})
            .limit(3)
            .sort("CreatedDateTime", -1)
        ):
            review_list.append(row)

    # get top 3 bookings (if available)
    booking = (
        Bookings.query.filter(
            Bookings.cid == current_user.get_id(), Bookings.date < date.today()
        )
        .order_by(Bookings.date.desc())
        .limit(3)
        .all()
    )

    for b in booking:
        data = {
            "bid": b.rid,
            "date": b.date,
            "time": b.time,
            "pax": b.pax,
            "special_request": b.special_request,
            "rid": b.rid,
            "created_at": b.created_at,
            "updated_at": b.updated_at,
        }
        print(data)
        booking_list.append(data)

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

    booking = (
        Bookings.query.filter(
            Bookings.cid == current_user.get_id(), Bookings.date < date.today()
        )
        .order_by(Bookings.date.desc())
        .all()
    )

    for b in booking:
        data = {
            "bid": b.rid,
            "date": b.date,
            "time": b.time,
            "pax": b.pax,
            "special_request": b.special_request,
            "rid": b.rid,
            "created_at": b.created_at,
            "updated_at": b.updated_at,
        }
        booking_list.append(data)

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
            "updated_at": o.updated_at,
        }
        order_list.append(data)

    # for testing
    o1 = {
        "orid": 1,
        "date": date.today(),
        "pickup_time": datetime.now(),
        "food_items": "idk a food",
        "special_request": "this is a request",
        "rid": 2,
        "created_at": datetime.now(),
    }
    order_list.append(o1)

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
            food_items=o.food_items,
            special_request=o.special_request,
            rid=o.rid,
        )

    # for testing
    order_item = Orders(
            orid=1,
            date=date.today(),
            pickup_time=datetime.now(),
            food_items="idk a food",
            special_request="this is a request",
            rid=2,
        )

    getRestaurantNames(restaurant_list)

    return render_template("profile/orderDetails.html", user=current_user, order=order_item, restaurants=restaurant_list)


# get all restaurant names
def getRestaurantNames(restaurant_list):
    restaurant = Restaurants.query.all()
    for r in restaurant:
        data = {"rid": r.rid, "name": r.name}
        restaurant_list.append(data)
