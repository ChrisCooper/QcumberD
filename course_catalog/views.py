# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import defaultdict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from course_catalog.models import Course, Subject, Term, Section, Career, Season
import model_controls


@cache_page(60 * 30)
def index(request):
    subject_list = Subject.objects.all().order_by('abbreviation')
    max_buckets = 9

    buckets = model_controls.subject_buckets(subject_list, max_buckets)

    if buckets == None:
        return render(request, 'course_catalog/pages/index.html')
    
    return render(request, 'course_catalog/pages/index.html',
        {'subject_buckets':buckets,
         'min_height': 50 + 29 * max([len(x[1]) for x in buckets])})


@cache_page(60 * 30)
def course_detail(request, subject_abbr=None, course_number=None):
    course = get_object_or_404(Course,
        subject__abbreviation__iexact=subject_abbr, number=course_number)

    sections = defaultdict(list)
    for section in course.sections.all().order_by('type__order'):
        sections[section.term].append(section)

    try:
        course_data = course.course_data
    except ObjectDoesNotExist as e:
        course_data = None

    textbooks = None
    exams = None
    if course_data:
        textbooks = course_data.textbooks
        exams = course_data.exams

    # Convert to a list of tuples for the template
    sections = sections.items()
    sections.sort(key=lambda t: t[0].order)

    return render(request, 'course_catalog/pages/course_detail.html',
        {'course': course, 'all_sections': sections,
        'textbooks': textbooks,
        'exams': exams},
        context_instance=RequestContext(request))


@cache_page(60 * 30)
def subject_detail(request, subject_abbr):
    subject = get_object_or_404(Subject, abbreviation__iexact=subject_abbr)

    # Since there are very few careers, we just get them all and filter later
    courses_by_career = []
    careers = Career.objects.all().order_by('order')

    for career in careers:
        c = subject.courses.filter(career=career).order_by('number')
        if c.count() != 0:
            courses_by_career.append((career, c))

    # Get seasons for the filter panel
    seasons = Season.objects.all().order_by('order')
    [setattr(s, 'checked', True) for s in seasons]

    return render(request, 'course_catalog/pages/subject_detail.html',
        {'subject': subject, 'courses_by_career': courses_by_career,
        'seasons': seasons})


@cache_page(60 * 30)
def search(request):
    query = request.GET.get('q')
    results = model_controls.search_result(query)

    if isinstance(results, models.Model):
        return HttpResponseRedirect(results.get_absolute_url())

    # Otherwise, it's a list of results
    for item in results:
        if isinstance(item, Course):
            item.template_name = "course_catalog/components/course_search_result.html"
        elif isinstance(item, Subject):
            item.template_name = "course_catalog/components/subject_search_result.html"
        elif isinstance(item, Section):
            item.template_name = "course_catalog/components/section_search_result.html"

    return render(request, 'course_catalog/pages/search_results.html',
        {'results': results, 'query': query})


# TODO: All these requests should be fixed up, since they just return simple
# responses.

@cache_page(60 * 30)
def about(request):
    return render(request, 'course_catalog/text/about.html')

@cache_page(60 * 30)
def contact(request):
    return render(request, 'course_catalog/text/contact.html')

@cache_page(60 * 30)
def tos(request):
    return render(request, 'course_catalog/text/tos.html', {})

@cache_page(60 * 30)
def faqs(request):
    return render(request, 'course_catalog/text/faqs.html', {})


# Application support

@cache_page(60 * 60 * 24 *100)
def facebook_channel(request):
    return render(request, 'course_catalog/text/channel.html', {})

@cache_page(60 * 60 * 24 *100)
def flash_permissions(request):
    return HttpResponse('')

@cache_page(60 * 30)
def robots(request):
    return render(request, 'course_catalog/text/robots.txt', {})


#For testing random things

def experiments(request):
    return render(request, 'course_catalog/experiments.html', {})
