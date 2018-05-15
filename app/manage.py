# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for,session, request
import random
import  os
import sys
from oauth import OAuthSignIn
import json
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.session import Session
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import Locations, Geodata, User
from config import Config
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from generator import GeoGen


app = Flask(__name__, static_url_path = "/assets" , static_folder='assets')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '156164541888335',
        'secret': 'cc23f5004b2e5536218a3206635b75bc'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }, 'google': {
            'id': '953536087639-c13jglsqemu2hf4ansq64a9rnmi9jofh.apps.googleusercontent.com',
            'secret': '-mgTCV7H5vtRk8UoWXp8qVZY'
        }
}

lm = LoginManager(app)
lm.login_view = 'index'

@app.route('/confirm_region/<region_id>')
def confirm_region(region_id):
    pass

@lm.user_loader
def get_user(ident):
  return User.query.get(int(ident))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('maps'))
    return  redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Look if the user already exists
    user=User.query.filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you 
        # require that.
        user=User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, True)
    return redirect(url_for('maps'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gen')
def gen():
    created = GeoGen(lat = "48.5206048429",lng = "32.2237075854")
    rezult  = created.save_city()
    return json.dumps(rezult) 

# localhost:5000/api/create_location?lat=48.5206048429&lng=32.2237075854
@app.route('/api/create_location')
def create_location():
    created = GeoGen(lat = str(request.args.get('lat')),lng = str(request.args.get('lng')))
    rezult  = created.save_city()
    return json.dumps(rezult)


@app.route('/check_region', methods=['GET','POST'])
def check_region():
    region_id = request.form["region_id"]
    if int(region_id) == int(session['region_id']):
        result = True
    else:
        result = False
    return json.dumps({'status':result})


@app.route('/get_region_city', methods=['GET','POST'])
def get_sity_by_region():
    region_id = request.form["region_id"]
    cityes = Geodata.query.filter_by(region_id=region_id).all()
    data = {}
    for item in cityes:
        data[str(item.id)] = item.title
    return json.dumps(data)


@app.route('/maps')
@login_required
def maps():
    regions = {

        '1': 'Харківська область',
        '2': 'Полтавська область',
        '3': 'Київська область',
        '4': 'Вінницька область',
        '5': 'Житомирська область',
        '6': 'Закарпатська область',
        '7': 'Хмельницька область',
        '8': 'АР Крим',
        '9': 'Запорізька область',
        '10': 'Херсонська область',
        '11': 'Одеська область',
        '12': 'Дніпропетровська область',
        '13': 'Чернігівська область',
        '14': 'Тернопільська область',
        '15': 'Донецька область',
        '16': 'Сумська область',
        '17': 'Кіровоградська область',
        '18': 'Черкаська область',
        '19': 'Миколаївська область',
        '20': 'Рівненська область',
        '21': 'Львівська область',
        '22': 'Волинська область',
        '24': 'Івано-Франківська область',
        '25': 'Чернівецька область',
    }
    if 'city_id' in session and 'lat' in session:
        data = {"lat": session['lat'], "lng": session['lng']}
    else:
        locate =  Locations.query.order_by(func.random()).first()
        session['region_id'] = locate.region_id
        session['city_id'] = locate.city_id
        session['lat'] = locate.latitude
        session['lng'] = locate.longitude

        data = {"lat": locate.latitude,"lng": locate.longitude}
    return render_template('maps.html',  data=data, regions=regions)

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0')
