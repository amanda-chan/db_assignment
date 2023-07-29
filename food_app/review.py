from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Customers, Bookings, Orders, Restaurants
from . import sql_db
from . import mongo_db
from pymongo import MongoClient


import json

review_bp = Blueprint("review", __name__, url_prefix="/review")


@review_bp.route("/make-a-review")
def make():
    # add login required
    # maybe need to add like booking = current booking then can, but now just try try to create
    return render_template("review/makeReview.html", user=current_user)


# there is a review tab in navbar, can view all reviews on that page:)
# user can see which review is positive then view that restaurant (idea you can consider)



#one other way is to fliter first, then i 
def retrieve_review():
    # retrieve all for testing first
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
    query = reviews_col.find({})

    review_list = []
    for record in query:

        review_list.append(record)
 
    return review_list


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

def filtered_res_reviews(restaurant):
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
  
    filter_query = ""
    if restaurant != "":
        filter_query = {"RID": restaurant}
    
    review_query = reviews_col.find(filter_query, {"_id": 0})
    review_f_list = []
    for record in review_query:   
        # object_id_str = str(record["_id"])      
        review_f_list.append(record)
        print(record)
    return review_f_list



#    #one other way is to fliter first, then i 
# def retrieve_flitered_review(review_query):
#     # retrieve all for testing first
#     myclient = MongoClient("mongodb://localhost:27017/")
#     db = myclient["db_project"]
#     reviews_col = db["reviews"]
#     query =review_query

#     review_list = []
#     for record in query:
#         print(record)
#         review_list.append(record)
#     print(review_list)
#     return review_list

# def filtered_reviews(rating, c_datetime, restaurant):
#     myclient = MongoClient("mongodb://localhost:27017/")
#     db = myclient["db_project"]
#     reviews_col = db["reviews"]
  
#     filter_query = {}
#     sort_query = []
#     if rating != "" and c_datetime != "" and restaurant != "":
           
#         filter_query = {"RID": restaurant}
#         sort_query.append(("Rating", -1 if rating == "high" else 1))
#         sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))

#     # only res is selected   
#     elif rating == "" and c_datetime == "" and restaurant != "":
#         filter_query = {"RID": restaurant}
            
#     # only rating is selected
#     elif rating != "" and c_datetime == "" and restaurant == "":
#         sort_query.append(("Rating", -1 if rating == "high" else 1))
    
#     review_query = reviews_col.find(filter_query).sort(sort_query)
   

    

        



@review_bp.route("/display", methods=["GET", "POST"])
def display():
    review_list = retrieve_review()
    # Gather all the restaurants with their details
    restaurant_list = retrieve_restaurants()

    if request.method == 'POST':
        review_list = []
        rating = request.form.get("rating")
        c_datetime = request.form.get("c_datetime")
        restaurant = request.form.get("restaurant")

        # if no fliter is applied
        if (rating == "" and c_datetime == "" and restaurant ==""):
            review_list = retrieve_review()

        # fliter based on what is selected
        else:
            # review_list =  filtered_reviews(rating, c_datetime, restaurant)
            # review_list = filtered_res_reviews(restaurant)
            review_list = filtered_res_reviews(restaurant)
            print("Form Data - Rating:", rating)
            print("Form Data - Date Time:", c_datetime)
            print("Form Data - Restaurant:", restaurant)
            print("Review List:", review_list)
            

        return render_template("review/showReviews.html", user=current_user, reviews=review_list, restaurants=restaurant_list)
    print("Review List:", review_list)
    return render_template("review/showReviews.html", user=current_user, reviews=review_list, restaurants=restaurant_list)

