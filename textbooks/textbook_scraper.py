# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import re
from bs4 import BeautifulSoup
from course_catalog.models import existing_or_new, Subject, Course
from models import Textbook


class TextbookScraper(object):

    def __init__(self, config):
        self.config = config

    def num_available(self, s):
        if s:
            #something funky going on with the "In Stock", couldn't get it to match
            m = re.search(".*\((\d+).*", s)
            return int(m.group(1)) if m else 0
        else:
            return 0

    def price(self, s):
        if s:
            m = re.search(".*(\$\d+\.\d{2}).*", s)
            return m.group(1) if m else None
        else:
            return None


    def scrape(self):

        print "Starting textbook scrape"

        print "Getting a list of courses"
        r = requests.get("http://www.campusbookstore.com/Textbooks/Booklists/")

        b = BeautifulSoup(r.text)
        content = b.find("div", {"class":"thecontent"})
        links  = content.find_all("a")

        temp = []

        for link in links:
            if "campusbookstore.com/Textbooks/Course/" in link.attrs.get("href", ""):
                m = re.search("^(\D+)(\d+).*$", link.string)
                # Only parse letters in config
                if m and m.group(1)[1].upper() in self.config.letters:
                    temp.append((m.group(1), m.group(2), link.attrs["href"]))

        print ("Parsing courses")
        for s, c, l in temp:

            # Check if there is a course to attach the book toexisting_or_new
            subject = Subject.existing(abbreviation=s)
            if not subject:
                continue
            course = Course.existing(subject=subject, number=c)
            if not course:
                continue

            print ("--Parsing " + s + " " + c)
            r = requests.get(l)
            b = BeautifulSoup(r.text)

            #looking at the page source, 49 books seems to be the limit (numbers padded the 2 digits)
            for i in range (0, 99, 2):

                book = b.find("div", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ModeFull".format(i)})
                if not book:
                    break

                print ("----Parsing book")

                temp = book.find("table").find("table").find_all("td")[1]

                # Title
                title = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_BookTitle".format(i)}).string
                
                # Authors
                authors = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_BookAuthor".format(i)}).string
                if authors and authors[:4] == " by ":
                    authors = authors[4:]

                # Required
                required = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_StatusLabel".format(i)}).string
                if required and "REQUIRED" in required.upper():
                    required = True
                else:
                    required = False

                # ISBN 13
                isbn_13 = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ISBN13Label".format(i)}).string
                if isbn_13 and "[N/A]" in isbn_13:
                    isbn_13 = None

                # ISBN 10
                isbn_10 = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ISBN10Label".format(i)}).string
                if isbn_10 and "[N/A]" in isbn_10:
                    isbn_10 = None
                
                # New data
                new_price = self.price(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_NewPriceLabel".format(i)}).string)
                new_available = self.num_available(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_NewAvailabilityLabel".format(i)}).string)
                
                # Used data
                used_price = self.price(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_UsedPriceLabel".format(i)}).string)
                used_available = self.num_available(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_UsedAvailabilityLabel".format(i)}).string)

                # Classifieds info
                classified_info = temp.find("a", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ClassifiedsLabel".format(i)}).string

                # Add the textbook
                if isbn_10 and isbn_13:

                    textbook_attrs = {
                        "title": title,
                        "authors": authors,
                        "required": required,
                        "isbn_10": isbn_10,
                        "isbn_13": isbn_13,
                        "new_price": new_price,
                        "new_available": new_available,
                        "used_price": used_price,
                        "used_available": used_available,
                        "classified_info": classified_info,
                        "course" : course,
                    }

                    # TODO: STACK OVERFLOW ERROR ON NEXT LINE
                    #textbook = existing_or_new(Textbook, **textbook_attrs)
                    #textbook.save()