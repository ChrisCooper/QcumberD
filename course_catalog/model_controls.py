# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import itertools
from course_catalog.models import Subject, Course

#assigns each split attempt a score
def split_score (split_points, num_items):
    best = num_items/len(split_points)
    score = 0
    for x in range(0, len(split_points)-1):
        score += abs(best - (split_points[x+1] - split_points[x]))
    return score

#returns a list containing lists of subjects
#the length of each list of subjects should be as close to equal as possible
#TODO: There has to be a faster way of doing this...
def subject_buckets(subjects, num_buckets):
    split_points = []
    best_split = []
    num_subjects = len(subjects)
    best_score = num_subjects

    #get availible split points
    for x in range(0, num_subjects-1):
        if subjects[x].abbreviation[0].upper() != subjects[x+1].abbreviation[0].upper():
            split_points.append(x+1)

    #iterate over split options
    for comb in itertools.combinations(split_points, num_buckets-1):
        temp = split_score(comb, num_subjects)
        if temp < best_score:
            best_split = comb
            best_score = temp
        if temp < 5: #good enough
            break;

    #return new list based on optimal split
    ret = [subjects[:best_split[0]]]
    for x in range(1, num_buckets-1):
        ret.append(subjects[best_split[x-1]:best_split[x]])
    ret.append(subjects[best_split[-1]:])

    return ret

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
            c = Course.objects.filter(subject__abbreviation__iexact=m.group(1), number__icontains=m.group(2)).order_by('number')
            if len(c) == 1:
                return c[0]
            elif c:
                return c
        except Course.DoesNotExist:
            pass
    else:
        #no numbers, so try a subject
        try:
            s = Subject.objects.get(abbreviation__iexact=str)
            return s
        except Subject.DoesNotExist:
            pass

    return full_search_result([str])


def double_word_search_result(words):
    #find courses
    try:
        c = Course.objects.filter(subject__abbreviation__iexact=words[0], number__contains=words[1])
        if len(c) == 1:
            return c[0]
        elif c:
            return c
    except Course.DoesNotExist:
        pass

    return full_search_result(words)


def full_search_result(words):
    return []
