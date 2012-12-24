from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

import json

from enrollment.models import SolusSession
from course_catalog.models import Section

def enrollment_numbers(request, subject_abbr, course_num, solus_id):
    section = get_object_or_404(Section, course__subject__abbreviation=subject_abbr, course__number=course_num, solus_id=solus_id)

    capacity, enrolled = SolusSession().scrape_enrollment(section)

    return HttpResponse(json.dumps({'enrolled': enrolled, 'capacity': capacity}))
