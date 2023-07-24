import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

sql_db = SQLAlchemy()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='some random string',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://db_project:password@localhost/foodappdb',
    )
    
    # init db
    sql_db.init_app(app)  


    # import blueprints
    from .auth import auth_bp
    from .home import home_bp
    from .profile import profile_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(profile_bp)

    from .models import Customer, Owner, Booking, Order, Restaurant

    with app.app_context():
        sql_db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(cid):
        return Customer.query.get(int(cid))

    return app

