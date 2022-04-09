from datetime import datetime

from sqlalchemy.orm import backref
from Halanweb import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    orders= db.relationship('Order',backref='author',lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Order(db.Model):
    client_contact_no= db.Column(db.String(10),nullable=False)
    order_id= db.Column(db.Integer,unique=True,primary_key=True,nullable=False)
    client_city=db.Column(db.String(150),nullable=False)
    client_address=db.Column(db.String(150),nullable=False)
    sme_name=db.Column(db.String(150),nullable=False)
    order_status=db.Column(db.String(150),nullable=True)
    order_reason_of_failure=db.Column(db.String(150),nullable=True)
    driver_name=db.Column(db.String(150),nullable=False)
    order_delivery_fees=db.Column(db.Float,nullable=False)
    order_value=db.Column(db.Float,nullable=False)
    order_date=db.Column(db.Date,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"Order('{self.order_id}', '{self.order_status}', '{self.order_value}', '{self.user_id}')"
   

    