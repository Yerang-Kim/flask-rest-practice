import os
from flask import Flask
from flask import render_template
from flask_jwt import JWT
from models import db, User
from api_v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/')
def hello():
    return render_template('home.html')

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMINT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sjsjijejiwcwqw'

db.init_app(app)
db.app = app
db.create_all()

def authenticate(username, password):
    user = User.query.filter(User.userid == username).first()
    if user.password == password:
        return user

def identity(payload):
    userid = payload['identity']
    return User.query.filter(User.id == userid).first()


jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)