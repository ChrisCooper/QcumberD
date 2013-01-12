import requests


class TextbookScraper(object):

    def __init__(self):
        pass

    def testing(self):

        r = requests.get("http://www.campusbookstore.com/Textbooks/Booklists/")
        return r.text
