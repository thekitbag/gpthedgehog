from webapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func


class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    subscription_type = db.Column(db.String(20), default='free')


    @classmethod
    def create_user(cls, first_name, last_name, email, password, subscription_type):
        hashed_password = generate_password_hash(password)
        new_user = cls(first_name=first_name, last_name=last_name, email=email, password=hashed_password, subscription_type=subscription_type)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, user, password):
        return check_password_hash(user.password, password)
    
    def get_current_month_search_count(self):
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        return db.session.query(func.count(Search.id)) \
                         .filter(Search.user_id == self.id) \
                         .filter(Search.timestamp >= current_month_start) \
                         .scalar()

    def __repr__(self):
        return f'<User {self.email}>'

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('searches', lazy=True))

    @classmethod
    def save_search(cls, user_id, query):
        search = cls(user_id=user_id, query=query)
        db.session.add(search)
        db.session.commit()
        return search