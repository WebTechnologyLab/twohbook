from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from flask_login import UserMixin
from hashlib import md5

starred = db.Table('starred',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(14), unique=True, index=True)
    name = db.Column(db.String(50))
    college = db.Column(db.String(100))
    branch = db.Column(db.String(10))
    year = db.Column(db.String(10))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seeen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    starred = db.relationship('Post', secondary=starred, backref=db.backref('starrers', lazy='dynamic'))

    def __repr__(self):
        return f'User <{self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def star(self, post):
        if not self.is_starred(post):
            self.starred.append(post)

    def unstar(self, post):
        if self.is_starred(post):
            self.starred.remove(post)

    def is_starred(self, post):
        return post in self.starred

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(64))
    year = db.Column(db.String(10))
    branch = db.Column(db.String(10))
    cost = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Post <{self.book_name}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
