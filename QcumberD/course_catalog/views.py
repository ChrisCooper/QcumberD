from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db import models
from course_catalog.models import Course, Subject, Term
import model_controls

def index(request):
    subject_list = Subject.objects.all().order_by('abbreviation')
    return render_to_response('course_catalog/pages/index.html', {'subject_list': subject_list})

def course_detail(request, subject_abbr=None, course_number=None):
    c = get_object_or_404(Course, subject__abbreviation__iexact=subject_abbr, number=course_number)
    terms = [s.term for s in c.sections.distinct('term')]
    terms.sort(key=lambda t: t.order)

    sections = []
    for t in terms:
        sections.append((t, c.sections.filter(term=t).order_by('type__order')))

    return render_to_response('course_catalog/pages/course_detail.html', {'course': c,
                                                                          'all_sections': sections})


def subject_detail(request, subject_abbr):
    s = get_object_or_404(Subject, abbreviation__iexact=subject_abbr)
    c = s.courses.order_by('number')
    return render_to_response('course_catalog/pages/subject_detail.html', {'subject': s,
                                                                     'courses': c})

def search(request):
    result = model_controls.search_result(request.GET.get('q'))

    if isinstance(result, models.Model):
        return HttpResponseRedirect(result.get_absolute_url())

    #Otherwise, it's a list of results

    return render_to_response('course_catalog/pages/subject_detail.html', {'subject': s,
                                                                     'courses': c})



#For testing random things
def experiments(request):
    return render_to_response('course_catalog/experiments.html', {})
