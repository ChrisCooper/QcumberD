from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from enrollment.models import SolusSession
from course_catalog.models import Section

def proof(request):

    section = get_object_or_404(Section, course__subject__abbreviation='CHEM', course__number='112A', solus_id='1757')

    #capacity, enrolled = SolusSession().scrape_enrollment(section)
    page = SolusSession().scrape_enrollment(section)

    return HttpResponse(page)
