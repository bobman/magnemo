from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask.ext.login import current_user
import os
import json
from flask_mail import Mail
import base64

def load_json():
    config={}
    if(not os.path.isfile("config.json")):
        create_json()
    with open("config.json") as data_file:
        config = json.load(data_file)
    return config

def create_json():
    tempConfig={
        "DEBUG": True,
        "SECRET_KEY": "super-secret",
        "SQLALCHEMY_DATABASE_URI":"sqlite:///magnemo.sqlite",
        "MAIL_SERVER": "mailserver",
        "MAIL_PORT": 587,
        "MAIL_USE_SSL": "True",
        "MAIL_USERNAME": "user@mailserver",
        "MAIL_PASSWORD": "secret"
    }
    with open("config.json","w") as data_file:
        json.dump(tempConfig,data_file)

# Create app
app = Flask(__name__)
myConfig=load_json()
app.config['DEBUG'] = myConfig['DEBUG']
app.config['SECRET_KEY'] = myConfig['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = myConfig['SQLALCHEMY_DATABASE_URI']
app.config['MAIL_SERVER'] = myConfig['MAIL_SERVER']
app.config['MAIL_PORT'] = myConfig['MAIL_PORT']
app.config['MAIL_USE_SSL'] = myConfig['MAIL_USE_SSL']
app.config['MAIL_USERNAME'] = myConfig['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = myConfig['MAIL_PASSWORD']
mail = Mail(app)
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Magnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.Text)
    top = db.Column(db.Integer)
    left = db.Column(db.Integer)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('magnets', lazy='dynamic'))

    def __init__(self,title,text,user,top,left,height,width):
        self.title=title
        self.text=text
        self.user=user
        self.top=top
        self.left=left
        self.height=height
        self.width=width

    def get_dataDict(self):
        magnetData = {
            "id":self.id,
            "title":self.title,
            "text":self.text,
            "top":self.top,
            "left":self.left,
            "height":self.height,
            "width":self.width
        }
        return magnetData

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
# @app.before_first_request
# def create_user():
   #db.create_all()
   # TODO: User creation via config file or installer
   #user_datastore.create_user(email='admin@localhost', password='admin')
   #db.session.commit()

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/magnets')
@login_required
def magnets():
    # m = Magnet("titel1","das ist der text",current_user,120,120,300,400)
    # m = Magnet("titel2","das ist der text",current_user,280,280,300,400)
    # db.session.add(m)
    # db.session.commit()
    data=[]
    
    for magnet in current_user.magnets.all():
        data.append(magnet.get_dataDict())

    return json.dumps(data)

@app.route('/magnet/<id>')
@login_required
def show_magnet(id):
    magnet = Magnet.query.filter(Magnet.user == current_user,Magnet.id == id).first()
    data=magnet.get_dataDict()
    return json.dumps(data)

@app.route('/magnet/<id>/edit', methods=['POST'])
@login_required
def update_magnet(id):

    magnet = Magnet.query.filter(Magnet.user == current_user,Magnet.id == id).first()
    magnet.top = request.form['top']
    magnet.left = request.form['left']
    magnet.height = request.form['height']
    magnet.width = request.form['width']
    db.session.commit()
    print(request.form['id'])
    return json.dumps("ok")


if __name__ == '__main__':
    app.run()