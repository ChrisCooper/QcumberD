from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_page

import json

from enrollment.models import SolusSession
from course_catalog.models import Section

@cache_page(60 * 1)
def enrollment_numbers(request, subject_abbr, course_num, solus_id):
    section = None
    try:
        section = Section.objects.get(course__subject__abbreviation=subject_abbr, course__number=course_num, solus_id=solus_id)
    except:
        return HttpResponse("There was a problem checking enrollment. This section might not exist anymore.")

    capacity, enrolled = (0,0)

    try:
        capacity, enrolled = SolusSession().scrape_enrollment(section)
    except:
        return HttpResponse("Sorry! There was a problem checking enrollment.")

    return render_to_response('enrollment/numbers.html', {'enrolled': enrolled, 'capacity': capacity})
