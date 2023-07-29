from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Customers, Bookings, Orders, Restaurants
from . import sql_db
from . import mongo_db
from pymongo import MongoClient
from bson import json_util
from datetime import datetime

import json

review_bp = Blueprint("review", __name__, url_prefix="/review")


# @review_bp.route("/makeReview", methods=["GET", "POST"])
# def make():
#     # add login required
#     # maybe need to add like booking = current booking then can, but now just try try to create
#     return render_template("review/makeReview.html", user=current_user)


# there is a review tab in navbar, can view all reviews on that page:)
# user can see which review is positive then view that restaurant (idea you can consider)
# get restaurant name
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

@review_bp.route("/makeReview", methods=["GET", "POST"])

def make():
    rid = request.args.get('rid')
    restaurant = Restaurants.query.get(rid)
    restaurant = restaurant
    my_review = request.form.get("review")
    my_rating_str =  request.form.get("rating")
    my_rating = 0
    if my_rating_str == "one":
        my_rating = 1
    elif my_rating_str == "two":
        my_rating = 2
    elif my_rating_str == "three":
        my_rating = 3
    elif my_rating_str == "four":
        my_rating = 4
    elif my_rating_str == "five":
        my_rating = 5
     
    now = datetime.now()
    c_time = now.strftime("%d/%m/%Y %H:%M:%S")
    reviewID = generate_newReviewID()

    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]

    record = {"review_id": reviewID ,"RID": int(rid), "CID": current_user.get_id(), "Review":my_review, "Rating":my_rating,"CreatedDateTime":c_time, "Comment":[] } 

    reviews_col.insert_one(record)
    return render_template("review/makeReview.html", user=current_user,restaurant = restaurant)
    # Gather all the restaurants with their details
    # restaurant_list = retrieve_restaurants()

    # if request.method == 'POST':
    #     filtered_reviews_list = [] 
    #     rating = request.form.get("rating")
    #     c_datetime = request.form.get("c_datetime")
    #     restaurant = request.form.get("restaurant")

    #     # if no fliter is applied
    #     if (rating == "" and c_datetime == "" and restaurant ==""):
    #         filtered_reviews_list = review_list

    #     # fliter based on what is selected
    #     else:
    #         # review_list =  filtered_reviews(rating, c_datetime, restaurant)
    #         # review_list = filtered_res_reviews(restaurant)
    #         # filtered_reviews = filtered_res_reviews(restaurant)
    #         filtered_reviews_list =  filtered_reviews(rating, c_datetime, restaurant)
    #         # filtered_reviews_list = filtered_reviews(c_datetime)
    #         print("Form Data - Rating:", rating)
    #         print(type(rating))
    #         print("Form Data - Date Time:", c_datetime)
    #         print("Form Data - Restaurant:", restaurant)
    #         print("Review List:", filtered_reviews_list)
            

    #     return render_template("review/showReviews.html", user=current_user, reviews=filtered_reviews_list, restaurants=restaurant_list)
    # # print("Review List:", review_list)
    # return render_template("review/showReviews.html", user=current_user, reviews=review_list, restaurants=restaurant_list)



#one other way is to fliter first, then i 
def retrieve_review():
    # retrieve all for testing first
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
    query = reviews_col.find({})

    review_list = []
    for record in query:
        sanitized_record = json.loads(json_util.dumps(record))
        review_list.append(sanitized_record)
 
    return review_list

def generate_newReviewID():
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
     # Sort documents based on "review_id" in ascending order
    query = reviews_col.find().sort("review_id", -1).limit(1)

    # Get the last document (highest review_id)
    last_review = query.next() 
    # if query.count_documents({}) > 0 else None
    if last_review:
        last_review_id = last_review["review_id"]
        new_reviewID = last_review_id + 1
        return new_reviewID
    else:
        # If the collection is empty, return a default value (e.g., 1)
        return 1

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


   #one other way is to fliter first, then i 
def retrieve_flitered_review(review_query):
    # retrieve all for testing first
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
    query =review_query

    review_list = []
    for record in query:
        print(record)
        review_list.append(record)
    print(review_list)
    return review_list

def filtered_reviews(rating, c_datetime, restaurant):
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
  
    filter_query = {}
    sort_query = []

    #if all fliters is selected
    if restaurant != "":
        filter_query = {"RID": int(restaurant)}
   
    if rating != "" and c_datetime != "":     
        sort_query.append(("Rating", -1 if rating == "high" else 1))
        sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))
    
    # only rating is selected
    elif rating != None:
        sort_query.append(("Rating", -1 if rating == "high" else 1))
    
    # only lastest or oldest review is selected is selected
    elif c_datetime != "":
        sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))

    # #only oldest or lastest review is selected
    # elif rating =="" and c_datetime != "" and  restaurant == "":
    #     sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))
    
    #  #only restaurant is selected
    # elif rating =="" and c_datetime == "" and  restaurant != "":
    #     filter_query = {"RID": int(restaurant)}

    # # only latest or oldest review is selected
    # elif rating ==""and c_datetime != "" and restaurant == "":
    #     sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))

   

    # rating and restaruant is selected
    # elif rating != "" and restaurant !="":
    #     filter_query = {"RID": int(restaurant)}
    #     sort_query.append(("Rating", -1 if rating == "high" else 1))


    # # rating and latest review or oldest review is selected
    # elif rating != "" and c_datetime !="":
    #     filter_query = {"RID": int(restaurant)}
    #     sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))
        
    # # restaurant and lastest or oldest review is selected
    # elif restaurant != "" and c_datetime !="":
    #     sort_query.append(("Rating", -1 if rating == "high" else 1))
    #     sort_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))
    # # only res is selected   
    # elif rating == "" and c_datetime == "" and restaurant != "":
    #     filter_query = {"RID": restaurant}
            
    # # only rating is selected
    # elif rating != "" and c_datetime == "" and restaurant == "":
    #     sort_query.append(("Rating", -1 if rating == "high" else 1))

    if filter_query and sort_query:
        review_query = reviews_col.find(filter_query).sort(sort_query)
    elif filter_query:
        review_query = reviews_col.find(filter_query)
    elif sort_query:
        review_query = reviews_col.find().sort(sort_query)
    else:
        review_query = reviews_col.find(filter_query)
    
    review_f_list = []
    for record in review_query:   
        sanitized_record = json.loads(json_util.dumps(record))     
        review_f_list.append(sanitized_record)
        print("Filtered Record:", sanitized_record)
    return review_f_list
   
def filtered_datetime_reviews(c_datetime):
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
  
    filter_query = {}
    sorted_query = []
    if c_datetime != "":
        sorted_query.append(("CreatedDateTime", -1 if c_datetime == "latest" else 1))
    
    review_query = reviews_col.find({}).sort(sorted_query)
    print(review_query)
    review_f_list = []
    for record in review_query:   
        sanitized_record = json.loads(json_util.dumps(record))     
        review_f_list.append(sanitized_record)
        print("Filtered Record:", sanitized_record)
    return review_f_list



@review_bp.route("/display", methods=["GET", "POST"])
def display():
    review_list = retrieve_review()
    # Gather all the restaurants with their details
    restaurant_list = retrieve_restaurants()

    if request.method == 'POST':
        filtered_reviews_list = [] 
        rating = request.form.get("rating")
        c_datetime = request.form.get("c_datetime")
        restaurant = request.form.get("restaurant")

        # if no fliter is applied
        if (rating == "" and c_datetime == "" and restaurant ==""):
            filtered_reviews_list = review_list

        # fliter based on what is selected
        else:
            # review_list =  filtered_reviews(rating, c_datetime, restaurant)
            # review_list = filtered_res_reviews(restaurant)
            # filtered_reviews = filtered_res_reviews(restaurant)
            filtered_reviews_list =  filtered_reviews(rating, c_datetime, restaurant)
            # filtered_reviews_list = filtered_reviews(c_datetime)
            print("Form Data - Rating:", rating)
            print(type(rating))
            print("Form Data - Date Time:", c_datetime)
            print("Form Data - Restaurant:", restaurant)
            print("Review List:", filtered_reviews_list)
            

        return render_template("review/showReviews.html", user=current_user, reviews=filtered_reviews_list, restaurants=restaurant_list)
    # print("Review List:", review_list)
    return render_template("review/showReviews.html", user=current_user, reviews=review_list, restaurants=restaurant_list)



