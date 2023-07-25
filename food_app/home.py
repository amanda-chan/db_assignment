from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from .models import Restaurant
from . import sql_db
from flask_sqlalchemy import SQLAlchemy

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@home_bp.route("/home")
@login_required
def home():
    return render_template("home/index.html")
