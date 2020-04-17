import os
from os.path import abspath, dirname

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash

basedir = abspath(dirname(__name__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()


# Model classes

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(16), nullable=False,
                         unique=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(64), nullable=False, unique=True)

    def verify_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.token = None

    def generate_token(self):
        pass

# APP ROUTES


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:username>')
def get_profile(username):
    pass


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/home')
def home():
    pass


# API endpoints

@app.route('/api/users', methods=["POST"])
def register_users():
    print(request.get_json())
    return render_template('index.html')


@app.route('/api/tokens', methods=["POST"])
def generate_tokens():
    pass


@app.route('/api/listings', methods=["GET"])
def provide_listings():
    pass


@app.route('/api/messages', methods=["GET", "POST"])
def message():
    pass


if __name__ == '__main__':
    app.run(debug=True)
