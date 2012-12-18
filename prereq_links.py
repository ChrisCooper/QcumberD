from django.core.management import setup_environ
import qcumber.settings as settings
setup_environ(settings)

import re, cgi

from course_catalog.models import Course

def link_requisites(c):
    s = cgi.escape(c.enrollment_reqs)
    matches = re.finditer("([A-Z]{3,4})\s*(\d{3}[AB]?)", s)

    #Because we are replacing strings as we go, the match indecies will become incorrect along the way
    index_offset = 0

    for match in matches:
        repr = '<a href="/search/?q=%s+%s">%s %s</a>' % (match.group(1), match.group(2), match.group(1), match.group(2))
        s = s[:match.start() + index_offset] + repr + s[match.end() + index_offset :]
        index_offset += len(repr) - len(match.group(0))
 
    c.enrollment_reqs = s
    c.save()

for c in Course.objects.all():
    link_requisites(c)