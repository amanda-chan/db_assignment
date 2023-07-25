from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Customer, Booking, Order, Restaurant
from . import sql_db
from . import mongo_db

review_bp = Blueprint("review", __name__, url_prefix="/review")


@review_bp.route("/make-a-review")
def make():
    # add login required
    #maybe need to add like booking = current booking then can, but now just try try to create
    return render_template("profile/review/makeReview.html", user=current_user)




# @review_bp.route("/")
# def review():
#     # add login required ^
#     return render_template("profile/reviews.html", user=current_user)