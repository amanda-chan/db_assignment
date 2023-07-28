from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Bookings, Restaurants
from . import sql_db, mongo_db


booking_bp = Blueprint("booking", __name__, url_prefix="/booking")

def retrieve_bookings():
    bookings_list = []
    all_bookings = Bookings.query.all() # Gather all bookings and their data

    for b in all_bookings:
        data = {
            'bid': b.rid,
            'date': b.date,
            'time': b.time,
            'pax': b.pax,
            'special_request': b.special_request,
            'created_at': b.created_at,
            'updated_at': b.updated_at
        }
        bookings_list.append(data)

    return bookings_list

# get all restaurant names
def getRestaurantNames(restaurant_list):
    restaurant = Restaurants.query.all()
    for r in restaurant:
        data = {
            "rid": r.rid,
            "name": r.name
        }
        restaurant_list.append(data)
    return restaurant_list



#View list of Bookings 
@booking_bp.route("/")
#@login_required
def view():
    #List of bookings of a cid
    bookings_list = []
    restaurant_list = []
    bookings_cid = Bookings.query.filter_by(cid=current_user.get_id()).all()

    for b in bookings_cid:
        data = {
            'bid': b.bid,
            'date': b.date,
            'time': b.time,
            'pax': b.pax,
            'special_request': b.special_request,
            'created_at': b.created_at,
            'updated_at': b.updated_at,
            "rid": b.rid
        }
        print(data)
        bookings_list.append(data)
    getRestaurantNames(restaurant_list)

    return render_template("booking/view.html", bookings_list = bookings_list, restaurants = restaurant_list, user = current_user)


#Create a new booking 
@booking_bp.route("/create-booking", methods=["GET", "POST"])
#@login_required
def make():
    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        pax = request.form.get("pax")
        special_request = request.form.get("special_request")
        restaurant = request.form.get("rid")

        new_booking = Bookings(
            date=date,
            time=time,
            pax=pax,
            special_request = special_request,
            created_at = datetime.now(),
            #add rid
            rid = restaurant,
            cid = current_user.get_id(),
        )
        sql_db.session.add(new_booking)
        sql_db.session.commit()
        #return redirect(url_for("booking.booking"))

    return render_template("booking/createBooking.html", user = current_user)

#Update
@booking_bp.route("/edit", methods=["GET", "POST"])
#@login_required
def edit():
    bid = request.args.get('bid')
    booking = Bookings.query.get(bid)
    restaurant_list = []
    getRestaurantNames(restaurant_list)

    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        pax = request.form.get("pax")
        special_request = request.form.get("special_request")
        
        booking = Bookings.query.get(bid)
        
        booking.date = date
        booking.time = time
        booking.pax = pax
        booking.special_request = special_request
        booking.updated_at = datetime.now()

        sql_db.session.commit()
        flash("Changes saved successfully!", category="success")
        return redirect(url_for("booking.view"))
    return render_template("booking/edit.html",booking = booking, restaurants = restaurant_list, user = current_user)

#Delete
@booking_bp.route("/delete", methods=["GET", "POST"])
#@login_required
def delete():
    bid = request.args.get('bid')
    booking = Bookings.query.get(bid)
    restaurant_list = []
    getRestaurantNames(restaurant_list)
    if request.method == "POST":

        booking=Bookings.query.get(bid)
        sql_db.session.delete(booking)

        sql_db.session.commit()
        flash("Deleted booking!", category="success")
        return redirect(url_for("booking.view"))

    return render_template("booking/delete.html", booking = booking, restaurants = restaurant_list, user = current_user)


