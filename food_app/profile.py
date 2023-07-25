from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Customer, Booking, Order, Restaurant
from . import sql_db

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/")
def profile():
    # add login required ^
    return render_template("profile/profile.html", user=current_user)


@profile_bp.route("/edit", methods=["GET", "POST"])
def edit():
    # add login required ^
    return render_template("profile/edit.html", user=current_user)


@profile_bp.route("/reviews")
def reviews():
    # add login required ^
    return render_template("profile/reviews.html", user=current_user, reviews=reviews)


@profile_bp.route("/bookings")
def bookings():
    # add login required ^
    return render_template("profile/bookings.html", user=current_user, bookings=bookings)


@profile_bp.route("/orders")
def orders():
    # add login required ^
    return render_template("profile/orders.html", user=current_user, orders=orders)
