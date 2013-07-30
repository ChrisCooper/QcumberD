from django.shortcuts import render
from course_catalog.models import Course
import prereqs.interface as parser

def index(request):
    # Display the parse everything 
    return render(request, 'prereqs/index.html', {})

def parse_all(request):
    parser.parse_all_courses()
    return render(request, 'prereqs/done.html', {})
