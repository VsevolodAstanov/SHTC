import re
import sys
import yaml
import argparse
import urllib.request
from urllib.parse import urlparse
from tkinter import *
from shtc import db
from shtc import tagparser
from datetime import datetime


class TagCounter():
    URL_REGXP = re.compile(
        r'^((?:http|ftp)s?://)?'  # http:// or https://
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # domain...
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        self.url = ''
        self.name = ''
        self.data = {}
        self.db = db.DB()

    def get_console_args(self):
        parser = argparse.ArgumentParser()
        commands = parser.add_mutually_exclusive_group()
        commands.add_argument('-g', '--get', nargs=1, metavar=('url'), help='get data directly using HTTP Request')
        commands.add_argument('-v', '--view', nargs=1, metavar=('url'), help='get data from DB')
        commands.add_argument('-d', '--delete', nargs=1, metavar=('url'), help='delete data from DB')
        args = parser.parse_args()

        ns = sys.argv

        if len(ns) > 1:
            url = str(ns[1:][1])
            self.parse_input_url(url)

        return args

    def get_http_data(self):
        html = self._http_request()
        tp = tagparser.TagParser()
        tp.feed(html)
        data = tp.get_tags()
        now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        insert_data = (self.name, self.url, now, str(data))
        self.db.insert(insert_data)
        self.view_db_data()

    def view_db_data(self):
        self.data = self.db.get(self.name)

    def delete_db_data(self):
        self.data = self.db.delete(self.name)

    def view_tags(self):
        print('Display Data: ' + str(self.data))

    def parse_input_url(self, inp):

        url = None

        if re.match(self.URL_REGXP, inp):
            up = urlparse(inp)
            if len(up.scheme) == 0:
                url = 'https://' + inp

        with open("synonyms.yml", 'r') as ymlfile:
            syn = yaml.load(ymlfile, Loader=yaml.FullLoader)

        for s in syn:
            if inp == s:
                url = syn[s]

        if url:
            self.url = url
            self.name = self._extract_domain(url)
        else:
            # Exception "Invalid URL or Synonym URL"
            print('URL is Invalid or no matches by synonyms')
            sys.exit()

    def _extract_domain(self, url):
        up = urlparse(url)
        domain = up.netloc.split(".")[-2]

        return domain

    def _http_request(self):
        with urllib.request.urlopen(self.url) as response:
            html = response.read().decode('utf-8')

        return html