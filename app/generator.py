# -*- coding: utf-8 -*-
import requests
from models import Locations, Geodata
import json
from flask.ext.sqlalchemy import SQLAlchemy


class GeoGen():

	lat = None
	lng = None
	type_loc = 0
 
	def __init__(self, lat,lng,type_loc):
		self.lat = lat
		self.lng = lng
		self.type_loc = type_loc
		self.db = db = SQLAlchemy()

	def geocode(self):
		url = 'https://maps.googleapis.com/maps/api/geocode/json?language=uk&latlng='+str(self.lat)+','+str(self.lng)+'&key=AIzaSyAqgxpxXFkQAO9zLCvMXSsaHUWkK_kZipo'
		print (url)
		response = requests.get(url)
		data = response.json()
		result  = data['results']
		return result

	def get_gmap_data(self, gmap_array):
		data = {}
		for item in gmap_array:
			if item['types'][0] == 'locality':
				data['city_name'] = item['address_components'][0]['short_name']
				data['region_name'] = item['address_components'][2]['short_name']
		return data

	def get_db_city(self, data):
  
		regions = {

			'Харківська область':'1',
			'Полтавська область':'2',
			'Київська область':'3',
			'місто Київ': '3',
			'Вінницька область':'4',
			'Житомирська область':'5',
			'Закарпатська область':'6',
			'Хмельницька область':'7',
			'АР Крим':'8',
			'Запорізька область':'9',
			 'Херсонська область':'10',
			 'Одеська область':'11',
			 'Дніпропетровська область':'12',
			 'Чернігівська область':'13',
			 'Тернопільська область':'14',
			 'Донецька область':'15',
			 'Сумська область':'16',
			 'Кіровоградська область':'17',
			 'Черкаська область':'18',
			 'Миколаївська область':'19',
			 'Рівненська область':'20',
			 'Львівська область':'21',
			 'Волинська область':'22',
			 'Івано-Франківська область':'24',
			 'Чернівецька область':'25',
		}
		if 'region_name' in data and data['region_name'].encode('utf-8') in regions:
			region_id = regions[data['region_name'].encode('utf-8')]
		else:
			return False
		print(region_id)
		city = Geodata.query.filter_by(title=data['city_name'].encode('utf-8'), region_id = int(region_id) ).first()
		if city is not None :
			new = Locations(
					region_id = region_id,
					city_id = int(city.id),
					latitude = self.lat,
					longitude = self.lng,
					type = self.type_loc,
				)
			self.db.session.add(new)
			self.db.session.commit()
			return city.id
		return False


	def save_city(self):
		data = self.get_gmap_data(self.geocode())
		city = self.get_db_city(data)
		if not city:
			return (data)
		return city
