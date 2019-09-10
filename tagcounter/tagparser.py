from html.parser import HTMLParser

class TagParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.tags = {}


    def handle_starttag(self, tag, args):
        self._store_tags(tag)


    def handle_startendtag(self, tag, args):
        self._store_tags(tag)


    def get_tags(self):
        return self.tags


    def _store_tags(self, tag):
        if tag in self.tags.keys():
            self.tags[tag] += 1
        else:
            self.tags[tag] = 1