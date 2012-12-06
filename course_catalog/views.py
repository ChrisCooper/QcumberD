from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db import models
from course_catalog.models import Course, Subject, Term, Section
import model_controls

def index(request):
    subject_list = Subject.objects.all().order_by('abbreviation')
    return render_to_response('course_catalog/pages/index.html', {'subject_list': subject_list})

def about(request):
    return render_to_response('course_catalog/pages/about.html')

def contact(request):
    return render_to_response('course_catalog/pages/contact.html')

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
    c = s.courses.order_by('career__order', 'number')
    return render_to_response('course_catalog/pages/subject_detail.html', {'subject': s,
                                                                     'courses': c})

def search(request):
    query = request.GET.get('q')
    results = model_controls.search_result(query)

    if isinstance(results, models.Model):
        return HttpResponseRedirect(results.get_absolute_url())

    #Otherwise, it's a list of results
    for item in results:
        if isinstance(item, Course):
            item.template_name = "course_catalog/components/course_search_result.html"
        elif isinstance(item, Subject):
            item.template_name = "course_catalog/components/subject_search_result.html"
        elif isinstance(item, Section):
            item.template_name = "course_catalog/components/section_search_result.html"

    return render_to_response('course_catalog/pages/search_results.html', {'results': results,
                                                                    'query': query})



#For testing random things
def experiments(request):
    return render_to_response('course_catalog/experiments.html', {})
