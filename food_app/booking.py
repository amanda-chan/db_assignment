from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Bookings, Restaurants
from . import sql_db, mongo_db
from datetime import datetime, timedelta


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


def generate_timings(operating_hours):
    
    timings_list = []

    # Varying operating hours
    if ", " in operating_hours:
        temp = operating_hours.split(", ")
        for time in temp:
            # Seperate start and end timings
            time_temp = time.split("-")
            start_time = datetime.strptime(time_temp[0], "%I:%M %p")
            end_time = datetime.strptime(time_temp[1], "%I:%M %p")

            # Add 30 mins intervals between operating hours
            interval_time = start_time
            while interval_time <= end_time:
                timings_list.append(interval_time.strftime("%I:%M %p"))
                interval_time += timedelta(minutes = 15)

    else:
        # Seperate start and end timings
        time_temp = operating_hours.split("-")
        start_time = datetime.strptime(time_temp[0], "%I:%M %p")
        end_time = datetime.strptime(time_temp[1], "%I:%M %p")
        
        # Check if the ending time is 12:00 AM - if so add one day
        if end_time.hour == 0 and end_time.minute == 0 and end_time.second == 0:
            end_time += timedelta(days = 1)

        # Add 30 mins intervals between operating hours
        interval_time = start_time
        while interval_time <= end_time:
            timings_list.append(interval_time.strftime("%I:%M %p"))
            interval_time += timedelta(minutes = 15)

    return timings_list

def validate_date(book_date, operating_days):

    avail_days = []
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Get the day of the week by date
    book_obj = datetime.strptime(book_date, "%Y-%m-%d")
    book_day = book_obj.weekday()
    book_day = week_days[book_day]

    # Gather the days opened in a list
    if ", " in operating_days:
        temp = operating_days.split(", ")
        for day in temp:
            if " - " in day:
                day_temp = day.split(" - ")
                index = week_days.index(day_temp[0])
                while index < len(week_days):
                    avail_days.append(week_days[index])
                    index += 1

            else:
                avail_days.append(day)

    else:
        day_temp = operating_days.split(" - ")
        index = week_days.index(day_temp[0])
        while index < len(week_days):
            avail_days.append(week_days[index])
            index += 1

    if book_day in avail_days:
        return True
    
    else:
        return False

    
#View list of Bookings 
@booking_bp.route("/")
def view():
    #List of bookings of a cid
    bookings_list = []
    bookings = sql_db.session.query(Bookings, Restaurants).join(Restaurants, Bookings.rid == Restaurants.rid).filter(Bookings.cid == current_user.cid).order_by(Bookings.date.asc()).all()

    # Get restaurant name and booking
    for b, r in bookings:
        data = {
                'bid': b.bid,
                'date': b.date,
                'time': b.time,
                'pax': b.pax,
                'special_request': b.special_request,
                "rid" : b.rid,
                "name" : r.name
        }
        bookings_list.append(data)

    return render_template("booking/view.html", bookings_list = bookings_list, user = current_user)


#Create a new booking 
@booking_bp.route("/create", methods=["GET", "POST"])
def create():
    restaurant_list = []
    rid = request.args.get('rid')
    restaurant = Restaurants.query.get(rid)
    selectedRname = restaurant.name
    selectedRrid = restaurant.rid
    getRestaurantNames(restaurant_list)

    timings_list = generate_timings(restaurant.operating_hours)
    days = restaurant.operating_days

    if request.method == "POST":
        date = request.form.get("date")
        bTime = request.form.get("time")
        pax = request.form.get("pax")
        special_request = request.form.get("special_request")
        restaurant = rid

        # Validate date
        validDate = validate_date(date, days)

        if not validDate:
            flash("Restaurant is not open on that date, please select another date", category = "error")

        else: 
            time = datetime.strptime(bTime, "%I:%M %p").time()
            new_booking = Bookings(
                date=date,
                time=time,
                pax=pax,
                special_request = special_request,
                created_at = datetime.now(),
                rid = restaurant,
                cid = current_user.get_id(),
            )
            sql_db.session.add(new_booking)
            sql_db.session.commit()
            flash("Booked successfully!", category="success")
            return redirect(url_for("booking.view"))

    return render_template("booking/create.html", selectedRid = selectedRrid, selectedName = selectedRname, rRid=rid, restaurants=restaurant_list, timings_list = timings_list, user = current_user)

#Update
@booking_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    bid = request.args.get('bid')
    booking_info = sql_db.session.query(Bookings, Restaurants).join(Restaurants, Bookings.rid == Restaurants.rid).filter(Bookings.bid == bid).first()
    booking, restaurant = booking_info


    r = restaurant.name
    timings_list = generate_timings(restaurant.operating_hours)
    days = restaurant.operating_days


    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        pax = request.form.get("pax")
        special_request = request.form.get("special_request")
        
        # Validate date
        validDate = validate_date(date, days)

        if not validDate:
            flash("Restaurant is not open on that date, please select another date", category = "error")

        else: 
            booking.date = date
            booking.time = time
            booking.pax = pax
            booking.special_request = special_request
            booking.updated_at = datetime.now()

            sql_db.session.commit()
            flash("Changes saved successfully!", category="success")
            return redirect(url_for("booking.view"))
    return render_template("booking/edit.html",booking = booking, rName = r, timings_list = timings_list, user = current_user)

#Delete
@booking_bp.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    bid = request.args.get('bid')
    booking_info = sql_db.session.query(Bookings, Restaurants).join(Restaurants, Bookings.rid == Restaurants.rid).filter(Bookings.bid == bid).first()
    booking, restaurant = booking_info
    r = restaurant.name

    if request.method == "POST":

        booking=Bookings.query.get(bid)
        sql_db.session.delete(booking)

        sql_db.session.commit()
        flash("Deleted booking!", category="success")
        return redirect(url_for("booking.view"))

    return render_template("booking/delete.html", booking = booking, rName = r, user = current_user)


