import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import mysql.connector
import pymongo
import pandas as pd

sql_db = SQLAlchemy()
migrate = Migrate()
mongo_db = pymongo.MongoClient()


def relational_db_setup():
    # Create connection object - change credentials accordingly
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root", 
        password = "root"
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


def restraunt_setup(sql_db, Restaurant):

    # Count number of rows in the Restaurant table
    count = Restaurant.query.count()

    if count == 0: # No existing data in the table, hence, populate the table
        print("Inserting data into the restaurants table...")

        # Extract data from the excel sheet
        df = pd.read_excel("food_app/data/restaurant_data.xlsx")

        # Replace NaN values in the 'email' column with an empty string
        df['email'].fillna('', inplace=True)

        # Replace NaN values in the 'contact_number' column with 0
        df['contact_number'].fillna('0', inplace=True)

        # Insert data rows into the table
        for index, row in df.iterrows():

            new_res = Restaurant(rid=int(row['rid']),
                                 name=row['name'],
                                 cuisine=row['cuisine'],
                                 operating_hours=row['operating_hours'],
                                 operating_days=row['operating_days'],
                                 address=row['address'],
                                 contact_number=int(row['contact_number']),
                                 email=row['email'],
                                 price=row['price'])
            
            sql_db.session.add(new_res)

        # Commit the changes to the database
        sql_db.session.commit()

    
def create_app():

    # Setup db if not yet
    relational_db_setup()
    mongo_db = nonrelational_db_setup()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='some random string',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://db_project:password@localhost/foodappdb',
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
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(profile_bp)
    app.register_blueprint(restaurant_bp)

    # create tables in the db
    from .models import Customer, Owner, Booking, Order, Restaurant

    with app.app_context():
        sql_db.create_all()
        # Initialise data
        restraunt_setup(sql_db, Restaurant)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(cid):
        return Customer.query.get(int(cid))

    return app

