from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Bookings
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

def retrieve_booking_byCID(c):
    bookings_list = []
    bookings_cid = Bookings.query.filter_by(cid=c).all()

    for b in bookings_cid:
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

#View list of Bookings 
@booking_bp.route("/")
#@login_required
def view():
    #List of bookings of a cid
    bookings_list = retrieve_booking_byCID(current_user.get_id())

    return render_template("booking/view.html", bookings_list = bookings_list, user = current_user)

#View a single booking info 
@booking_bp.route("/info")
#@login_required
def info():
    bid = request.args.get('bid')
    booking = Bookings.query.get(bid)

    return render_template("booking/info.html", booking = booking, user = current_user)


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
    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        pax = request.form.get("pax")
        special_request = request.form.get("special_request")
        restaurant = request.form.get("rid")
        
        booking = Bookings.query.get(bid)
        
        booking.date = date
        booking.time = time
        booking.pax = pax
        booking.special_request = special_request
        booking.rid = restaurant
        booking.updated_at = datetime.now()

        sql_db.session.commit()
        #return redirect(url_for("booking.booking"))
    return render_template("booking/edit.html", user = current_user)

#Delete
@booking_bp.route("/delete")
#@login_required
def delete():
    bid = request.args.get('bid')
    #delete function here

    return render_template("booking/delete.html", user = current_user)


