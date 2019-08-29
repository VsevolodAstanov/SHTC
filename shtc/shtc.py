import sys
import argparse
import urllib.request
from tkinter import *
from shtc import tagparser
from shtc import gui

class TagCounter():

    def __init__(self):
        self.url = ''
        self.gui = True
        self.tagData = {}

    def run(self):
        parser = argparse.ArgumentParser()
        commands = parser.add_mutually_exclusive_group()
        commands.add_argument('--get', nargs=1, metavar=('url'), help='get data directly using HTTP Request')
        commands.add_argument('--view', nargs=1, metavar=('url'), help='get data from DB')
        args = parser.parse_args()

        ns = sys.argv
        if len(ns) > 1:
            self.gui = False
            url = str(ns[1:][1])

            #ValIdate URL

            self.url = url


        if args.get:
            self.getData()
        elif args.view:
            self.viewData()
        else:
            gui
            print("Run GUI")


    def getData(self):
        print('Get ' + self.url)
        html = self._httpRequest()
        tp = tagparser.TagParser()
        tp.feed(html)


    def viewData(self):
        print('View ' + self.url)


    def _httpRequest(self):
        with urllib.request.urlopen(self.url) as response:
            html = response.read().decode('utf-8')

        return html


    def _validateURL(self):
        print("Validate URL")