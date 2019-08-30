import re
import sys
import argparse
import urllib.request
from tkinter import *
from shtc import tagparser
from urllib.parse import urlparse


class TagCounter():

    URL_REGXP = re.compile(
        r'^((?:http|ftp)s?://)?'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


    def __init__(self):
        self.url = ''
        self.data = {}


    def get_console_args(self):
        parser = argparse.ArgumentParser()
        commands = parser.add_mutually_exclusive_group()
        commands.add_argument('--get', nargs=1, metavar=('url'), help='get data directly using HTTP Request')
        commands.add_argument('--view', nargs=1, metavar=('url'), help='get data from DB')
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
        self.data = tp.get_tags()
        #store data to DB


    def get_db_data(self):
        self.data = "DB Data"


    def view_tags(self):
        print('Display ' + str(self.data))


    def parse_input_url(self, url):

        if re.match(self.URL_REGXP, url):
            up = urlparse(url)
            if len(up.scheme) == 0:
                url = 'https://' + url

            self.url = url
            return

        # Get Data from yaml File

        #if suff is not in yaml
        #Exception "Invalid URL or Synonym URL"

        return url


    def _extract_domain(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc.split(".")[1:]

        return domain


    def _http_request(self):
        with urllib.request.urlopen(self.url) as response:
            html = response.read().decode('utf-8')

        return html


    def _validate_url(self):
        print("Validate URL")