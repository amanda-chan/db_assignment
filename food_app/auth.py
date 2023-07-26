from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Customers
from werkzeug.security import generate_password_hash, check_password_hash
from . import sql_db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Customers.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("home.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("auth/login.html", user=current_user)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        contact_number = request.form.get("contact-number")

        user = Customers.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 3:
            flash("Email must be at least 3 characters.", category="error")
        elif len(username) < 3:
            flash("First name must be at least 3 character.", category="error")
        elif password != confirm_password:
            flash("Passwords don't match.", category="error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", category="error")
        elif re.search("^[89][0-9]{7}$", str(contact_number)) is None:
            flash("Please enter a valid local phone number.", category="error")
        else:
            new_user = Customers(
                email=email,
                username=username,
                password=generate_password_hash(password, method="sha256"),
                contact_number=contact_number,
            )
            sql_db.session.add(new_user)
            sql_db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for("home.home"))

    return render_template("auth/register.html", user=current_user)
