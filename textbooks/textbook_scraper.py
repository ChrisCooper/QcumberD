# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import re
from bs4 import BeautifulSoup
from course_catalog.models import existing_or_new, Subject, Course
from models import Textbook, TextbookRelation
from django.core.exceptions import ObjectDoesNotExist


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

            # Check if there is a course to attach the book to
            subject = None
            course = None
            try:
                subject = Subject.objects.get(abbreviation=s)
                course = Course.objects.get(subject=subject, number=c)
            except ObjectDoesNotExist:
                print ("No course '{0} {1}' in database".format(s, c))
                continue

            print ("--Parsing books from " + str(course))
            r = requests.get(l)
            b = BeautifulSoup(r.text)

            # Create the course <-> textbook relation
            ct_relation = existing_or_new(TextbookRelation, course=course, listing_url=l)
            ct_relation.save()

            # Looking at the page source, 49 books seems to be the limit (numbers padded the 2 digits)
            for i in range (0, 99, 2):

                book = b.find("div", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ModeFull".format(i)})
                if not book:
                    break

                temp = book.find("table").find("table").find_all("td")[1]

                textbook_attrs = {}

                # Title
                title = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_BookTitle".format(i)}).string
                textbook_attrs["title"] = unicode(title)

                # Authors
                authors = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_BookAuthor".format(i)}).string
                if authors and authors[:4] == " by ":
                    textbook_attrs["authors"] = authors[4:]

                # Required
                required = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_StatusLabel".format(i)}).string
                if required and "REQUIRED" in required.upper():
                    textbook_attrs["required"] = True

                # ISBN 13
                isbn_13 = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ISBN13Label".format(i)}).string
                if isbn_13 and "[N/A]" in isbn_13:
                    textbook_attrs["isbn_13"] = None
                else:
                    textbook_attrs["isbn_13"] = unicode(isbn_13)

                # ISBN 10
                isbn_10 = temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ISBN10Label".format(i)}).string
                if isbn_10 and "[N/A]" in isbn_10:
                    textbook_attrs["isbn_10"] = None
                else:
                    textbook_attrs["isbn_10"] = unicode(isbn_10)
                
                # New data
                new_price = self.price(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_NewPriceLabel".format(i)}).string)
                new_available = self.num_available(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_NewAvailabilityLabel".format(i)}).string)
                if new_price:
                    textbook_attrs["new_price"] = new_price
                if new_available:
                    textbook_attrs["new_available"] = new_available
                
                # Used data
                used_price = self.price(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_UsedPriceLabel".format(i)}).string)
                used_available = self.num_available(temp.find("span", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_UsedAvailabilityLabel".format(i)}).string)
                if used_price:
                    textbook_attrs["used_price"] = used_price
                if used_available:
                    textbook_attrs["used_available"] = used_available

                # Classifieds info
                classified_info = temp.find("a", {"id": "ctl00_ContentBody_ctl00_CourseBooksRepeater_ctl{:02d}_test_ClassifiedsLabel".format(i)}).string
                if classified_info:
                    textbook_attrs["classified_info"] = classified_info

                # Add the textbook
                if textbook_attrs["isbn_10"] or textbook_attrs["isbn_13"]:

                    textbook = existing_or_new(Textbook, **textbook_attrs)
                    textbook.course_rels.add(ct_relation)
                    textbook.save()
                    print "----Parsed book:"
                    print ("------" + str(textbook))