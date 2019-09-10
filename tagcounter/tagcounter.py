import re
import sys
import yaml
import json
import argparse
import pkg_resources
import urllib.request
import urllib.error
from urllib.parse import urlparse
from tagcounter.logger import Logger
from tagcounter.patterns import Singleton
from tabulate import tabulate
from datetime import datetime
from tagcounter.db import DB
from tagcounter.tagparser import TagParser


class TagCounter(metaclass=Singleton):
    URL_REGXP = re.compile(
        r'^((?:http|ftp)s?://)?'  # http:// or https://
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # domain...
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        super().__init__()
        self.log = Logger()()
        self.url = ''
        self.name = ''
        self.data = None
        self.isGUI = True
        self.db = DB()

    def get_data(self):
        return self.data

    def get_console_args(self):
        try:
            self.log.info('GET CONSOLE ARGUMENTS')

            parser = argparse.ArgumentParser()
            commands = parser.add_mutually_exclusive_group()
            commands.add_argument('-g', '--get', nargs=1, metavar='url', help='get data directly using HTTP Request')
            commands.add_argument('-v', '--view', nargs=1, metavar='url', help='get data from DB')
            commands.add_argument('-d', '--delete', nargs=1, metavar='url', help='delete data from DB')
            args = parser.parse_args()

            ns = sys.argv

            if len(ns) > 1:
                self.isGUI = False
                url = str(ns[1:][1])
                if not self.parse_input_url(url):
                    sys.exit()

            return args
        except Exception as err:
            self.log.critical('Cannot parse console arguments: ' + str(err))

            if not self.isGUI:
                sys.exit()

    def get_http_data(self):
        try:
            self.log.info('GET HTTP DATA FOR: ' + str(self.url))

            self.data = None

            html = self._http_request()
            if not html:
                raise ValueError('Unable to get HTML')

            tp = TagParser()
            tp.feed(html)
            tags = tp.get_tags()

            now = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            data = (self.name, self.url, now, json.dumps(tags),)
            self.db.insert(data)
            self.data = data
        except ValueError as err:
            self.log.critical(str(err))

            if not self.isGUI:
                sys.exit()

    def get_db_data(self):
        try:
            self.log.info('GET DB DATA FOR: ' + str(self.url))

            self.data = None
            data = self.db.get(self.name, self.url)

            if data:
                self.data = data
            else:
                raise ValueError('No required data in DB')
        except ValueError as err:
            self.log.warning(str(err))

    def delete_db_data(self):
        self.db.delete(self.name)

    def display(self):
        try:
            self.log.info('DISPLAY CONSOLE DATA')

            if self.data:

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
            else:
                raise ValueError('No data to display with requested url')
        except ValueError as err:
            self.log.critical(str(err))

    def parse_input_url(self, inp):
        try:
            self.log.info('PARSE URL')
            self.url = ''
            self.name = ''

            if re.match(self.URL_REGXP, inp):
                up = urlparse(inp)
                if len(up.scheme) != 0:
                    self.url = inp
                else:
                    self.url = 'https://' + inp

            synms = self._get_synonyms()

            for s in synms:
                if inp == s:
                    self.url = synms[s]

            if self.url:
                self.name = self._extract_domain()
                self.log.debug('URL: ' + self.url + ' / NAME: ' + self.name)

                return True
        except:
            self.log.warning('Unable to parse URL: ' + str(inp))
            return False

    def _get_synonyms(self):
        try:
            self.log.info('Open "synonyms.yml" file')

            file_path = pkg_resources.resource_filename(__name__, 'synonyms.yml')
            self.log.debug('Synonym File Path: ' + str(file_path))

            with open(file_path, 'r') as ymlfile:
                syn = yaml.load(ymlfile, Loader=yaml.FullLoader)

            ymlfile.close()

            return syn
        except FileNotFoundError as err:
            self.log.warning('Unable to open synonyms.yml file: ' + str(err))

    def _extract_domain(self):
        try:
            up = urlparse(self.url)
            domain = up.netloc.split(".")[-2]

            return domain
        except:
            self.log.critical('Unable to extract domain: ' + str(sys.exc_info()[1]))

    def _http_request(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                html = response.read().decode('utf-8')

            return html
        except:
            self.log.warning('No HTTP connection: ' + str(sys.exc_info()[1]))
