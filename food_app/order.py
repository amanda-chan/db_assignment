from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Restaurants, Orders
from . import sql_db, mongo_db
from datetime import datetime, timedelta

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

            # Add 30 mins intervals between the pickup times during operating hours
            interval_time = start_time
            while interval_time <= end_time:
                timings_list.append(interval_time.strftime("%I:%M %p"))
                interval_time += timedelta(minutes = 30)

    else:
        # Seperate start and end timings
        time_temp = operating_hours.split("-")
        start_time = datetime.strptime(time_temp[0], "%I:%M %p")
        end_time = datetime.strptime(time_temp[1], "%I:%M %p")
        
        # Check if the ending time is 12:00 AM - if so add one day
        if end_time.hour == 0 and end_time.minute == 0 and end_time.second == 0:
            end_time += timedelta(days = 1)

        # Add 30 mins intervals between the pickup times during operating hours
        interval_time = start_time
        while interval_time <= end_time:
            timings_list.append(interval_time.strftime("%I:%M %p"))
            interval_time += timedelta(minutes = 30)

    return timings_list

def validate_date(pickup_date, operating_days):

    avail_days = []
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Get the day of the week by date
    pickup_obj = datetime.strptime(pickup_date, "%Y-%m-%d")
    pickup_day = pickup_obj.weekday()
    pickup_day = week_days[pickup_day]

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

    if pickup_day in avail_days:
        return True
    
    else:
        return False


@order_bp.route("/")
def view():

    # Gather restaurants thats only can be ordered from
    restaurant_list = get_restaurants()

    return render_template("order/view.html", restaurant_list = restaurant_list, user = current_user)

@order_bp.route("/make-an-order", methods=['GET', 'POST'])
@login_required
def create():

    rid = request.args.get('rid')

    # Get restaurant information
    restaurant = Restaurants.query.get(rid)

    # Get menu collections from the db
    menu = mongo_db["menu"]

    # Get menu from chosen restaurant
    query_rid = { "RID" : int(rid) }
    menu_items = menu.find(query_rid)

    # Get pickup time within operating hours
    timings_list = generate_timings(restaurant.operating_hours)

    # Set pickup date max as 2 weeks from the next day
    # Set pickup date min to be the next day
    today = datetime.today()
    date_min = today + timedelta(days = 1) 
    date_max = date_min + timedelta(weeks = 2)
    date_min = date_min.date()
    date_max = date_max.date()

    if request.method == 'POST':

        food_items = []

        for m in menu_items:
            item = m['MenuItem']
            quantity = int(request.form.get(str(m['item_id'])))

            if quantity > 0: # Customer ordered menu item
                food_dict = { "item" : item, "quantity" : quantity}
                food_items.append(food_dict)

        pickup_date = request.form.get("pickup-date")
        pickup_time = request.form.get("pickup-time")
        special_request = request.form.get("special-request")

        # Check if date is valid during operating days
        validity = validate_date(pickup_date, restaurant.operating_days)

        if food_items == []:
            flash("No food options selected", category = "error")

        elif not validity:
            flash("Restaurant is not open on that date, please select another date", category = "error")

        else:
            pickup_time = datetime.strptime(pickup_time, "%I:%M %p").time()
            # Add into database
            new_order = Orders(date=pickup_date,
                               pickup_time=pickup_time,
                               food_items=str(food_items),
                               special_request=special_request,
                               rid=int(rid),
                               cid=current_user.cid)
            sql_db.session.add(new_order)
            sql_db.session.commit()
            flash("Order placed successfully!", category = "success")

        # Render menu again
        query_rid = { "RID" : int(rid) }
        menu_items = menu.find(query_rid)



    return render_template("order/create.html", restaurant = restaurant, menu_items = menu_items, timings_list = timings_list, date_min = date_min, date_max = date_max, user = current_user)

@order_bp.route("/view-orders", methods=['GET', 'POST'])
@login_required
def view_orders():
    
    order_list = []

    # Get user's current orders
    orders = Orders.query.filter_by(cid=current_user.cid).all()

    # Get restaurant name and order info
    for o in orders:

        # Get restaurant information
        restaurant = Restaurants.query.get(o.rid)

        order_dict = {"oid" : o.orid,
                      "name" : restaurant.name,
                      "date" : o.date,
                      "time" : o.pickup_time,
                      "food_items" : eval(o.food_items)}
        
        order_list.append(order_dict)

    
    for i in order_list:
        print(type(i['food_items']))
        for h in i['food_items']:
            print(h['item'])



    return render_template("order/view_orders.html", order_list=order_list, user = current_user)