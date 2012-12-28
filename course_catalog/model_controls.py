# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from course_catalog.models import Subject, Course

#returns a list containing lists of subjects
#the length of each list of subjects should be as close to equal as possible
#format [(name, [list of subjects]), ...]
def subject_buckets(subjects, max_buckets):
    num_subjects = len(subjects)
    opt_bucket = num_subjects//max_buckets

    #No subjects, no buckets
    if len(subjects) == 0:
        return None

    #get availible split points (between letters)
    split_points = []
    for x in range(0, num_subjects-1):
        if subjects[x].abbreviation[0].upper() != subjects[x+1].abbreviation[0].upper():
            split_points.append(x+1)

    #No split points? No problem!
    if len(split_points) == 0:
        return [["", subjects]]

    #Find the number of items between each split point
    num_in_splits = [split_points[0]] + \
                    [split_points[x+1] - split_points[x] for x in range(0, len(split_points) - 1)] + \
                    [num_subjects - split_points[-1]]

    #Optimally combine split points
    curr = num_in_splits[0]
    best_split = []
    for x in range(1, len(num_in_splits)):
        if len(best_split) == max_buckets - 2:
            #last split, try to equalize the 2 buckets
            #index is x-1 because we're not counting the previous curr value
            closer = False
            
            #rolling counts
            temp1 = num_in_splits[x-1]
            temp2 = sum(num_in_splits[x:])

            #store best
            best_diff = sum(num_in_splits[x-1:])
            best1 = temp1
            best2 = temp2
            
            for y in range(x, len(num_in_splits)):
                #rolling counts
                temp1 += num_in_splits[y]
                temp2 -= num_in_splits[y]

                diff = abs(temp2 - temp1)
                if diff < best_diff:
                    best_diff = diff
                    best1 = temp1
                    best2 = temp2
                    closer = True #should always be getting closer now
                elif closer:
                    #gone too far, stop looking
                    break
            best_split.append(best1)
            best_split.append(best2)
            break
        #The +2 makes the algorithm err on the side of less, resulting in a more even distribution
        elif abs(opt_bucket - curr) < abs(opt_bucket - (curr + num_in_splits[x])) + 2:
            best_split.append(curr)
            curr = num_in_splits[x]
        else:
            curr += num_in_splits[x]
    else:
        #NOTE: Not going to return the max number of buckets
        best_split.append(curr)

    #return new list based on optimal split
    start = 0
    ret = []
    for x in best_split[:-1]:
        #add tuple of name and subject list
        ret.append((subjects[start].abbreviation[0].upper() + "-" + \
                    subjects[start + x - 1].abbreviation[0].upper(),
                    subjects[start:start + x]))
        start += x
    #add the last one (*-Z)
    ret.append((subjects[start].abbreviation[0].upper() + "-Z", subjects[start:]))

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
