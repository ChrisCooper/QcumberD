import requests
from bs4 import BeautifulSoup


class TextbookScraper(object):

    def __init__(self):
        pass

    def testing(self):

        r = requests.get("http://www.campusbookstore.com/Textbooks/Booklists/")

        b = BeautifulSoup(r.text)
        content = b.find("div", {"class":"thecontent"})
        links  = content.find_all("a")

        temp = []

        for link in links:
            if "campusbookstore.com/Textbooks/Course/" in link.attrs.get("href", ""):
                temp.append((link.string, link.attrs["href"]))

        return "</br>".join([n + " ---> " + l for n, l in temp])
