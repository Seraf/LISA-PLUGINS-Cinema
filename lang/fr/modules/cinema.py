# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from lisa import configuration

class Cinema:
    def __init__(self):
        self.configuration_lisa = configuration
        mongo = MongoClient(self.configuration_lisa['database']['server'], \
                            self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "Cinema"})

    def getFilms(self):
        film_str = ""
        for salle in self.configuration['configuration']['salles']:
            if salle['enabled'] == 'True':
                film_str += u" Dans la salle "+ salle['name'] +u" sont joués les films : "
                #lxml improve speed but need to be installed
                #soup = BeautifulSoup(urllib.urlopen(configuration['url_' + salle['type']] + salle['id']),"lxml")
                soup = BeautifulSoup(urllib.urlopen(self.configuration['configuration']['url_' + salle['type']] + salle['id']))
                if salle['type'] == "Gaumont":
                    film_str += u' puis '.join(unicode(film.get_text()) for film in soup.find_all("p", class_="titre"))
        return json.dumps({"plugin": "Cinema", "method": "getFilms", "body": film_str})
