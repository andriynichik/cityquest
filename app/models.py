from flask.ext.sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, nullable=False, unique=True)
    city_id = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(64), nullable=True)
    longitude = db.Column(db.String(64), nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self,  region_id, city_id, latitude, longitude):

        self.region_id = region_id
        self.city_id =city_id
        self.latitude = latitude
        self.longitude = longitude



  

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    def __init__(self, id):
        self.id = id

class Geodata(db.Model):
    __tablename__ = 'geodata'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, nullable=False, unique=True)
    lat = db.Column(db.String(64), nullable=True)
    lng = db.Column(db.String(64), nullable=True)
    title = db.Column(db.String(64), nullable=True)

    def __init__(self, id):
        self.id = id
