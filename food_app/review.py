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


@review_bp.route("/display", methods=["GET", "POST"])
def display():
    review_list = retrieve_review()
    return render_template("profile/review.showReviews.html", reviews=review_list)


# there is a review tab in navbar, can view all reviews on that page:)
# user can see which review is positive then view that restaurant (idea you can consider)


def retrieve_review():
    # retrieve all for testing first
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["db_project"]
    reviews_col = db["reviews"]
    query = reviews_col.find({})

    review_list = []
    for record in query:
        print(record)
        review_list.append(record)

    return review_list


# @review_bp.route("/")
# def review():
#     # add login required ^
#     return render_template("profile/reviews.html", user=current_user)
