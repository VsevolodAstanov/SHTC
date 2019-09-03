import re
import sys
import yaml
import json
import argparse
import urllib.request
from urllib.parse import urlparse
from tabulate import tabulate
from datetime import datetime
from shtc import db
from shtc import tagparser


class TagCounter():
    URL_REGXP = re.compile(
        r'^((?:http|ftp)s?://)?'  # http:// or https://
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # domain...
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        self.url = ''
        self.name = ''
        self.data = None
        self.db = db.DB()

    def get_data(self):
        return self.data

    def get_console_args(self):
        print('Logging [SHTC]: Parse Console Arguments')
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
        print('Logging [SHTC]: Get Data using HTTP Request')
        html = self._http_request()
        tp = tagparser.TagParser()
        tp.feed(html)
        tags = tp.get_tags()
        now = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        data = (self.name, self.url, now, json.dumps(tags),)
        self.db.insert(data)
        self.data = data


    def get_db_data(self):
        data = self.db.get(self.name)

        if data:
            self.data = data
            print('Logging [SHTC]: Set data from DB')
        else:
            self.data = None
            print('Exception [SHTC]: No Data to Display')

    def delete_db_data(self):
        self.db.delete(self.name)
        print('Logging [SHTC]: Delete Data from DB')

    def display(self):
        name = self.data[0]
        url = self.data[1]
        date = self.data[2]
        tags = json.loads(self.data[3])

        dt = []
        for t in tags:
            dt.append([t, tags[t]])

        print('\nName: ' + name +
              '\nURL: ' + url +
              '\nLast Update: ' + date +
              '\n' + tabulate(dt, headers=['Tag', 'Amount']))

    def parse_input_url(self, inp):
        try:
            url = None

            if re.match(self.URL_REGXP, inp):
                up = urlparse(inp)
                if len(up.scheme) != 0:
                    url = inp
                else:
                    url = 'https://' + inp

            with open('synonyms.yml', 'r') as ymlfile:
                syn = yaml.load(ymlfile, Loader=yaml.FullLoader)

            for s in syn:
                if inp == s:
                    url = syn[s]

            if url:
                self.url = url
                self.name = self._extract_domain(url)
            else:
                raise NotImplementedError("Invalid URL or Synonym URL")

        except Exception as err:
            print(err)
            return False

    def _extract_domain(self, url):
        up = urlparse(url)
        domain = up.netloc.split(".")[-2]

        return domain

    def _http_request(self):
        with urllib.request.urlopen(self.url) as response:
            html = response.read().decode('utf-8')

        return html
