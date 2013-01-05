# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db import models
from course_catalog.models import Course, Subject, Term, Section
import model_controls
from django.views.decorators.cache import cache_page
from django.template import RequestContext


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
    c = get_object_or_404(Course,
        subject__abbreviation__iexact=subject_abbr, number=course_number)
    terms = [s.term for s in c.sections.distinct('term')]
    terms.sort(key=lambda t: t.order)

    sections = []
    for t in terms:
        secs = c.sections.filter(term=t).order_by('type__order')
        secs = sorted(secs, key=lambda s: s.type.order)
        sections.append((t, secs))

    return render(request, 'course_catalog/pages/course_detail.html',
        {'course': c, 'all_sections': sections},
        context_instance=RequestContext(request))


@cache_page(60 * 30)
def subject_detail(request, subject_abbr):
    s = get_object_or_404(Subject, abbreviation__iexact=subject_abbr)

    careers = [c.career for c in s.courses.distinct('career')]

    careers = sorted(careers, key=lambda c: c.order if c else 0)

    c = [(career, s.courses.filter(career=career).order_by('number')) for career in careers]

    return render(request, 'course_catalog/pages/subject_detail.html',
        {'subject': s, 'courses_by_career': c})


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
