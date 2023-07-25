from . import sql_db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Customer(sql_db.Model, UserMixin):
    cid = sql_db.Column(sql_db.Integer, primary_key=True)
    email = sql_db.Column(sql_db.String(150), unique=True, nullable=False)
    username = sql_db.Column(sql_db.String(20), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(225), nullable=False)
    contact_number = sql_db.Column(sql_db.Integer, nullable=False)
    created_at = sql_db.Column(sql_db.DateTime(timezone=True), default=func.now())
    updated_at = sql_db.Column(sql_db.DateTime(timezone=True))
    bookings = sql_db.relationship("Booking", backref="customer", passive_deletes=True)
    orders = sql_db.relationship("Order", backref="customer", passive_deletes=True)

    def get_id(self):
        return self.cid


class Owner(sql_db.Model):
    oid = sql_db.Column(sql_db.Integer, primary_key=True)
    email = sql_db.Column(sql_db.String(150), unique=True, nullable=False)
    first_name = sql_db.Column(sql_db.String(20), unique=True, nullable=False)
    last_name = sql_db.Column(sql_db.String(20), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(225), nullable=False)
    contact_number = sql_db.Column(sql_db.Integer, nullable=False)
    created_at = sql_db.Column(sql_db.DateTime(timezone=True), default=func.now())
    updated_at = sql_db.Column(sql_db.DateTime(timezone=True))
    restaurants = sql_db.relationship('Restaurant', backref='owner', passive_deletes=True)


class Restaurant(sql_db.Model):
    rid = sql_db.Column(sql_db.Integer, primary_key=True)
    name = sql_db.Column(sql_db.String(225), unique=True, nullable=False)
    cuisine = sql_db.Column(sql_db.String(500), nullable=False)
    operating_hours = sql_db.Column(sql_db.String(100), nullable=False)
    operating_days = sql_db.Column(sql_db.String(50), nullable=False)
    address = sql_db.Column(sql_db.String(500), nullable=False)
    contact_number = sql_db.Column(sql_db.Integer)
    email = sql_db.Column(sql_db.String(150))
    price = sql_db.Column(sql_db.String(10), nullable=False)
    oid = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('owner.oid'))


class Booking(sql_db.Model):
    bid = sql_db.Column(sql_db.Integer, primary_key=True)
    date = sql_db.Column(sql_db.Date(), nullable=False)
    time = sql_db.Column(sql_db.Time(), nullable=False)
    pax = sql_db.Column(sql_db.Integer, nullable=False)
    special_request = sql_db.Column(sql_db.String(500))
    created_at = sql_db.Column(sql_db.DateTime(timezone=True), default=func.now())
    updated_at = sql_db.Column(sql_db.DateTime(timezone=True))
    rid = sql_db.Column(sql_db.Integer, sql_db.ForeignKey("restaurant.rid"))
    cid = sql_db.Column(sql_db.Integer, sql_db.ForeignKey("customer.cid"))


class Order(sql_db.Model):
    orid = sql_db.Column(sql_db.Integer, primary_key=True)
    date = sql_db.Column(sql_db.Date(), nullable=False)
    pickup_time = sql_db.Column(sql_db.Time(), nullable=False)
    food_items = sql_db.Column(sql_db.String(225), nullable=False)
    special_request = sql_db.Column(sql_db.String(500))
    created_at = sql_db.Column(sql_db.DateTime(timezone=True), default=func.now())
    rid = sql_db.Column(sql_db.Integer, sql_db.ForeignKey("restaurant.rid"))
    cid = sql_db.Column(sql_db.Integer, sql_db.ForeignKey("customer.cid"))
