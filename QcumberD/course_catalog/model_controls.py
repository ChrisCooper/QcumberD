import re
from course_catalog.models import Subject, Course

def search_result(str):

    words = str.split()
    if len(words) == 1:
        return single_word_search_result(str)
    elif len(words) == 2:
        return double_word_search_result(words)
    
    return []

def single_word_search_result(str):
    #try to match e.g. 'cisc101'
    m = re.match(r'(\D+)(\d+.*)', str)

    if m:
        #find courses
        try:
            c = Course.objects.filter(subject__abbreviation__iexact=m.group(1), number__contains=m.group(2))
            if len(c) == 1:
                return c[0]
            elif c:
                return c
        except Course.DoesNotExist:
            pass
    else:
        #no numbers, so try a subject
        try:
            s = Subject.objects.get(abbreviation=str)
            return s
        except Subject.DoesNotExist:
            pass

    return full_search_result(str)


def double_word_search_result(words):
    return []

def full_search_result(words):
    return []