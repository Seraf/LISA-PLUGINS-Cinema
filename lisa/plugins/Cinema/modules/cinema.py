# -*- coding: UTF-8 -*-
import urllib
from bs4 import BeautifulSoup

from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os


class Cinema(IPlugin):
    def __init__(self):
        super(Cinema, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "Cinema"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = translation = gettext.translation(domain='cinema',
                                                   localedir=self.path,
                                                   fallback=True,
                                                   languages=[self.configuration_lisa['lang']]).ugettext

    def getFilms(self, jsonInput):
        film_str = ""
        for salle in self.configuration_plugin['configuration']['salles']:
            if salle['enabled'] == 'True':
                film_str += self._('In the theater are played these films: ') % salle['name']
                #lxml improve speed but need to be installed
                #soup = BeautifulSoup(urllib.urlopen(configuration['url_' + salle['type']] + salle['id']),"lxml")
                soup = BeautifulSoup(urllib.urlopen(self.configuration_plugin['configuration']['url_' + salle['type']] + salle['id']))
                if salle['type'] == "Gaumont":
                    film_str += self._(' then ').join(unicode(film.get_text()) for film in soup.find_all("p", class_="titre"))
        return {"plugin": "Cinema",
                "method": "getFilms",
                "body": film_str
        }
