from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from course_catalog.models import Course

def new_job(request):
    return HttpResponse('Begining scrape pass')