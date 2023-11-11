import random
import os
import base64
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User info: {self.id}|{self.first_name}|{self.last_name}|{self.address}|{self.phone_number}|{self.date_created}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'phone_number': self.phone_number,
            'date_created': self.date_created
        }
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password', ''))

    
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

    def get_token(self):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(hours=1)
        db.session.commit()
        return self.token
        

@login.user_loader
def get_user(user_id):
    return db.session.get(User, user_id)

def random_photo():
    random_number = random.randint(1,1000)
    return f"https://picsum.photos/500?random={random_number}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String, default=random_photo)

    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'image_url': self.image_url
        }
