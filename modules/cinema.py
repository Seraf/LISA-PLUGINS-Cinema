# -*- coding: UTF-8 -*-
import urllib, json, os, inspect
from bs4 import BeautifulSoup
from pymongo import MongoClient
from lisa import configuration

import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='cinema', localedir=path, languages=[configuration['lang']]).ugettext

class Cinema:
    def __init__(self, lisa):
        self.lisa = lisa
        self.configuration_lisa = configuration
        mongo = MongoClient(self.configuration_lisa['database']['server'],
                            self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "Cinema"})

    def getFilms(self, jsonInput):
        film_str = ""
        for salle in self.configuration['configuration']['salles']:
            if salle['enabled'] == 'True':
                film_str += _('In the theater are played these films: ') % salle['name']
                #lxml improve speed but need to be installed
                #soup = BeautifulSoup(urllib.urlopen(configuration['url_' + salle['type']] + salle['id']),"lxml")
                soup = BeautifulSoup(urllib.urlopen(self.configuration['configuration']['url_' + salle['type']] + salle['id']))
                if salle['type'] == "Gaumont":
                    film_str += _(' then ').join(unicode(film.get_text()) for film in soup.find_all("p", class_="titre"))
        return {"plugin": "Cinema",
                "method": "getFilms",
                "body": film_str
        }
