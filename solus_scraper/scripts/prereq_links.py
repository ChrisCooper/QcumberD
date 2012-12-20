from django.core.management import setup_environ
import qcumber.settings as settings
setup_environ(settings)

import re

from course_catalog.models import Subject, Course

s = "Prerequisite of (MBIO218 & CHEM222 &223) or CHEM282 Exclusion: no more than 6.0 units from BCHM310; BCHM315; BCHM316 Exclusion: No more than 3.0 units from BCHM102; BCHM310; BCHM315; BCHM316"
s2 = "Prerequisite CLST200/3.0 or CLST201/3.0 or CLST207/3.0 or CLST208/3.0"

matches = re.finditer("([A-Z]{3,4})\s*(\d{3}[AB]?)", s)

#Because we are replacing strings as we go, the match indecies will become incorrect along the way
index_offset = 0

for match in matches:
    repr = '<a href="/search/?q=%s+%s>%s %s</a>' % (match.group(1), match.group(2), match.group(1), match.group(2))
    s = s[:match.start() + index_offset] + repr + s[match.end() + index_offset :]
    index_offset += len(repr) - len(match.group(0))


print s

#m.start(0), m.end(0)) for m in re.finditer(pattern, string)
