import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import mysql.connector
import pymongo
import pandas as pd
import json
from werkzeug.security import generate_password_hash

sql_db = SQLAlchemy()
migrate = Migrate()
myclient = pymongo.MongoClient()
mongo_db = myclient["db_project"]


def relational_db_setup():
    # Create connection object - change credentials accordingly
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="root"
    )

    cursor = mydb.cursor()

    # Create foodappdb if it does not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS foodappdb;")

    # Check if user db_project exists
    cursor.execute("SELECT User FROM mysql.user WHERE User = 'db_project';")
    result = cursor.fetchall()

    if not result:
        print("User - db_project does not exists, creating and granting permissions...")
        cursor.execute("CREATE USER 'db_project'@'localhost' IDENTIFIED BY 'password';")
        cursor.execute("GRANT ALL ON foodappdb.* TO 'db_project'@'localhost';")


def nonrelational_db_setup():
    # Connect Non-relational Database to LocalHost
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # Init database
    mydb = myclient["db_project"]

    return mydb


def restraunt_setup(sql_db, Restaurants):
    # Count number of rows in the Restaurant table
    count = Restaurants.query.count()

    if count == 0:  # No existing data in the table, hence, populate the table
        print("Inserting data into the restaurant table...")

        # Extract data from the excel sheet
        df = pd.read_excel("food_app/data/restaurant_data_v3.xlsx")

        # Replace NaN values in the 'email' column with an empty string
        df["email"].fillna("", inplace=True)

        # Replace NaN values in the 'contact_number' column with 0
        df["contact_number"].fillna("0", inplace=True)

        # Insert data rows into the table
        for index, row in df.iterrows():
            new_res = Restaurants(
                rid=int(row["rid"]),
                name=row["name"],
                cuisine=row["cuisine"],
                operating_hours=row["operating_hours"],
                operating_days=row["operating_days"],
                address=row["address"],
                contact_number=int(row["contact_number"]),
                email=row["email"],
                price=row["price"],
                oid=row["oid"],
            )

            sql_db.session.add(new_res)

        # Commit the changes to the database
        sql_db.session.commit()


def owner_setup(sql_db, Owners):
    # Count number of rows in the Owner table
    count = Owners.query.count()

    if count == 0:  # No existing data in the table, hence, populate the table
        print("Inserting data into the owner table...")

        # Extract data from the excel sheet
        df = pd.read_excel("food_app/data/owner_data_v2.xlsx")

        # Insert data rows into the table
        for index, row in df.iterrows():
            new_owner = Owners(
                oid=int(row["oid"]),
                email=row["email"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                password=generate_password_hash(row["password"], method="sha256"),
                contact_number=row["contact_number"],
            )

            sql_db.session.add(new_owner)

        # Commit the changes to the database
        sql_db.session.commit()


def customer_setup(sql_db, Customers):
    # Count number of rows in the Customers table
    count = Customers.query.count()

    if count < 50:  # No existing data in the table, hence, populate the table
        print("Inserting data into the customer table...")

        # Extract data from the excel sheet
        df = pd.read_excel("food_app/data/customer_data.xlsx")

        # Insert data rows into the table
        for index, row in df.iterrows():
            customer = Customers(
                cid=int(row["cid"]),
                email=row["email"],
                username=row["username"],
                password=generate_password_hash(row["password"], method="sha256"),
                contact_number=row["contact_number"],
            )

            sql_db.session.add(customer)

        # Commit the changes to the database
        sql_db.session.commit()


def menu_setup(mongo_db):
    # Create or switch to menu collection
    menu = mongo_db["menu"]

    # Get the first document
    result = menu.find_one()

    if result == None:  # No existing data in the collection, hence populate data
        print("Inserting data into the menu collection...")

        # Extract data from json file
        with open("food_app/data/menu_data.json") as file:
            file_data = json.load(file)

        # Insert menu data into menu collection
        menu.insert_many(file_data)


def reviews_setup(mongo_db):
    # Create or switch to reviews collection
    reviews = mongo_db["reviews"]

    # Get the first document
    result = reviews.find_one()

    if result == None:  # No existing data in the collection, hence populate data
        print("Inserting data into the reviews collection...")

        # Extract data from json file
        with open("food_app/data/review_data.json") as file:
            file_data = json.load(file)

        # Insert review data into reviews collection
        reviews.insert_many(file_data)


def booking_history_setup(mongo_db):

    # Create or switch to reviews collection
    bookings = mongo_db["bookingHistory"]

    # Get the first document
    result = bookings.find_one()

    if result == None: # No existing data in the collection, hence populate data
        print("Inserting data into the booking history collection...")

        # Extract data from json file
        with open("food_app/data/booking_history_data.json") as file:
            file_data = json.load(file)

        # Insert review data into reviews collection
        bookings.insert_many(file_data)


def bookings_setup(sql_db, Bookings):
    # Count number of rows in the Restaurant table
    count = Bookings.query.count()

    if count == 0:  # No existing data in the table, hence, populate the table
        print("Inserting data into the bookings table...")

        # Extract data from the excel sheet
        df = pd.read_excel("food_app/data/booking_data.xlsx")

        # Replace NaN values in the 'email' column with an empty string
        df["special_request"].fillna("", inplace=True)
        df["updated_at"].fillna("", inplace=True)
        df["updated_at"] = df["updated_at"].astype(str).replace({"NaT": None})
        # Insert data rows into the table
        for index, row in df.iterrows():
            new_booking = Bookings(
                bid=int(row["bid"]),
                date=row["date"],
                time=row["time"],
                pax=int(row["pax"]),
                special_request=row["special_request"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                rid=int(row["rid"]),
                cid=int(row["cid"]),
            )

            sql_db.session.add(new_booking)

        # Commit the changes to the database
        sql_db.session.commit()

def order_setup(sql_db, Orders):
    # Count number of rows in the Orders table
    count = Orders.query.count()

    if count == 0:  # No existing data in the table, hence, populate the table
        print("Inserting data into the orders table...")

        # Extract data from the excel sheet
        df = pd.read_excel("food_app/data/order_data.xlsx")

        # Replace NaN values in the 'special_request' column with an empty string
        df["special_request"].fillna("", inplace=True)

        # Insert data rows into the table
        for index, row in df.iterrows():
            order = Orders(
                orid=int(row["orid"]),
                date=row["date"],
                pickup_time=row["pickup_time"],
                food_items=row["food_items"],
                special_request=row["special_request"],
                rid=int(row["rid"]),
                cid=int(row["cid"]),
                )

            sql_db.session.add(order)

        # Commit the changes to the database
        sql_db.session.commit()


def create_app():
    # Setup db if not yet
    relational_db_setup()
    mongo_db = nonrelational_db_setup()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="some random string",
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://db_project:password@localhost/foodappdb",
    )

    # init db
    sql_db.init_app(app)

    # migration - for any changes in the db
    migrate.init_app(app, sql_db)

    # import blueprints
    from .auth import auth_bp
    from .home import home_bp
    from .profile import profile_bp
    from .restaurant import restaurant_bp
    from .order import order_bp
    from .review import review_bp
    from .booking import booking_bp
    from .search import search_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(profile_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(search_bp)

    # create tables in the db
    from .models import Customers, Owners, Bookings, Orders, Restaurants

    with app.app_context():
        sql_db.create_all()
        # Initialise data
        owner_setup(sql_db, Owners)
        restraunt_setup(sql_db, Restaurants)
        customer_setup(sql_db, Customers)
        bookings_setup(sql_db, Bookings)
        order_setup(sql_db, Orders)
        menu_setup(mongo_db)
        reviews_setup(mongo_db)
        booking_history_setup(mongo_db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(cid):
        return Customers.query.get(int(cid))

    return app
