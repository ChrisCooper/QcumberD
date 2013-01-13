import requests
import re
from bs4 import BeautifulSoup


class TextbookScraper(object):

    def __init__(self):
        pass

    def num_available(self, s):
        if s:
            #something funky going on with the "In Stock", couldn't get it to match
            m = re.search(".*\((\d+).*", s)
            return int(m.group(1)) if m else 0
        else:
            return 0


    def testing(self):

        r = requests.get("http://www.campusbookstore.com/Textbooks/Booklists/")

        b = BeautifulSoup(r.text)
        content = b.find("div", {"class":"thecontent"})
        links  = content.find_all("a")

        temp = []

        for link in links:
            if "campusbookstore.com/Textbooks/Course/" in link.attrs.get("href", ""):
                m = re.search("^(\D+)(\d+).*$", link.string)
                if m:
                    temp.append((m.group(1), m.group(2), link.attrs["href"]))

        print ("Parsing courses")
        for s, c, l in temp:
            print ("--Parsing " + s + " " + c)
            r = requests.get(l)
            b = BeautifulSoup(r.text)

            #looking at the code, 49 books seems to be the limit (numbers padded the 2 digits)
            for i in range (0, 99, 2):

                book = b.find("div", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ModeFull".format(i)})
                if not book:
                    break

                print ("----Parsing book")

                temp = book.find("table").find("table").find_all("td")[1]

                title = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_BookTitle".format(i)}).string
                
                authors = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_BookAuthor".format(i)}).string
                if not authors:
                    authors = None
                elif authors[:4] == " by ":
                    authors = authors[4:]

                required = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_StatusLabel".format(i)}).string
                if "REQUIRED" in required.upper():
                    required = True
                else:
                    required = False

                isbn13 = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ISBN13Label".format(i)}).string
                if "[N/A]" in isbn13:
                    isbn13 = None

                isbn10 = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ISBN10Label".format(i)}).string
                if "[N/A]" in isbn10:
                    isbn10 = None
                
                #size can be 'Small', 'Medium', or 'Large'
                imageURL = "http://www.campusbookstore.com/image.aspx?size=Medium&isbn=" + (isbn13 if isbn13 else isbn10)

                newPrice = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_NewPriceLabel".format(i)}).string
                if not re.search("^\$\d+\.\d{2}$", newPrice):
                    newPrice = None

                newNumAvailable = self.num_available(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_NewAvailabilityLabel".format(i)}).string)
                
                usedPrice = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_UsedPriceLabel".format(i)}).string
                if not re.search("^\$\d+\.\d{2}$", usedPrice):
                    usedPrice = None
                
                usedNumAvailable = self.num_available(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_UsedAvailabilityLabel".format(i)}).string)

                classifieds = temp.find("a", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ClassifiedsLabel".format(i)}).string
                classifiedsURL = "http://www.campusbookstore.com/Textbooks/Usedbooks/Buy/?isbn=" + (isbn13 if isbn13 else isbn10)
   
                #print "--------------------------"
                #print "------Title: " + str(title)
                #print "------Authors: " + str(authors)
                #print "------Required?: " + str(required)
                #print "------ISBN13: " + str(isbn13)
                #print "------ISBN10: " + str(isbn10)
                #print "------New price: " + str(newPrice)
                #print "------# New avaiable: " + str(newNumAvailable)
                #print "------Used price: " + str(usedPrice)
                #print "------# Used available: " + str(usedNumAvailable)
                #print "------Classified info: " + str(classifieds)
                #print "------Link to classifieds: " + str(classifiedsURL)
                #print "------Image URL: " + str(imageURL)
                #print "--------------------------"
