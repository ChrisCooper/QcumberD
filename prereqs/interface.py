# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

#####################
# IMPORT STATEMENTS #
#####################


import json

from prereqs import parser, generator
from django.core.exceptions import ObjectDoesNotExist

from course_catalog.models import Course

######################
# EXPORTED FUNCTIONS #
######################

###
# Parsing Course Prerequisites
###


def parse_course(course):
    """
    Parses the Prerequisite text of the passed course generating
    a parsed json version, and saving it in the database
    """

    parsed = parser.parse(course.enrollment_reqs)
    parsed_text = json.dumps(parsed, indent=4)
    course.parsed_reqs = parsed_text

    course.save()


def parse_all_courses():
    """
    Parses the prerequisite text of all courses and generates
    a parsed json version, saving it in the database
    """

    courses = Course.objects.all()
    for course in courses:
        parse_course(course)


###
# Generating Prerequisite Graphs
###


def generate_prereq_graph(subject, number):
    """
    Generates a prerequisite graph for the passed course
    returns the graph in dotfile format
    """

    # Determine the courses' name
    coursename = '%s %s' % (subject, number)

    # Generate the set of nodes
    nodes = {}
    generator.generate_course(coursename, nodes, prereqs)

    # Return the dotfile form of the set of nodes
    return generator.to_dot(nodes)


def prereqs(subject, coursenum):
    """
    Returns a dictionary version of the parsed requisites
    If the course doesn't exist, returns None
    """

    try:
        course = Course.objects.get(subject__abbreviation=subject,
                                    number=coursenum)
        return json.loads(course.parsed_reqs)
    except ObjectDoesNotExist:
        # There is no such subject
        return
    except ValueError:
        # The subject doesn't have valid json requirements
        return
