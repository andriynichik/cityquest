# -*- coding: utf-8 -*-
import requests
from .models import Locations, Geodata

class GeoGen(object):

    def __init__(self, lat,lng):
         self.lat = lat
         self.lat = lng
    def search_place(self):

        pass

    def get_city(self):
         return self.lat