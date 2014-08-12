from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

import prereqs.interface as parser


@staff_member_required
def index(request):
    # Display the parse everything link
    return render(request, 'prereqs/index.html', {})


@staff_member_required
def parse_all(request):
    parser.parse_all_courses()
    return render(request, 'prereqs/done.html', {})
