from html.parser import HTMLParser

class TagParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = {}


    def handle_starttag(self, tag, args):
        if tag in self.data.keys():
            self.data[tag] += 1
        else:
            self.data[tag] = 1


    def handle_startendtag(self, tag, args):
        if tag in self.data.keys():
            self.data[tag] += 1
        else:
            self.data[tag] = 1


    def get_data(self):
        return self.data