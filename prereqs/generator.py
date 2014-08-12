# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

#####################
# IMPORT STATEMENTS #
#####################

# JSON is required to make node names
import json
import hashlib

try:
    from django.core.urlresolvers import reverse
except:
    # Try to load reverse in if running in django
    pass

######################
# EXPORTED FUNCTIONS #
######################


def generate_course(coursename, nodes, prereqs):
    """
    Generates the nodes for a specific course.

    must be passed a nodes dictionary to add the course
    node to.

    prereqs(subject, coursenum) 
        => Dict generated by parser for course, if it exists
        => Falsey value otherwise
    """

    # Don't create a node if it has already been created
    if coursename in nodes:
        return coursename

    # Create the node
    nodes[coursename] = {'label': coursename}

    # Determine the subject & the course number
    if coursename.find(' ') is -1:
        return coursename
    subject, coursenum = coursename.split(' ')

    # Generate prerequisite nodes
    course = prereqs(subject, coursenum)
    if course:
        for kind in ['prerequisite', 'corequisite', 'recommend']:
            if kind in course:
                node = course[kind]
                if node['type'] == 'or':
                    node = {
                        'type': 'and',
                        'items': [node]
                    }
                generate_node(node, kind, nodes, prereqs, coursename)

    return coursename


def generate_node(source, kind, nodes, prereqs, name=None):
    """
    Generates a specific row.

    must be passed a nodes dictionary to add the course
    node to.

    prereqs(subject, coursenum) 
        => Dict generated by parser for course, if it exists
        => Falsey value otherwise
    """

    # Generate a name if it is not set
    if name is None:
        # Name is generated by dumping a json form, and then sha224 hashing it
        # This means that identical ands and ors will not be created
        name = str(hashlib.sha224(json.dumps(source)).hexdigest())
        label = source['type'].upper()
    else:
        label = name

    # Create the node if it doesn't already exist
    if not name in nodes:
        # We have not already generated that node
        nodes[name] = {
            kind: [],
            'label': label
        }
    else:
        nodes[name][kind] = []

    # Go through each of the items in the prerequisite tree
    for item in source['items']:
        if type(item) is dict:
            # This is an and/or - recurse
            nodes[name][kind].append(
                generate_node(item, kind, nodes, prereqs)
            )
        else:
            # This is a course
            nodes[name][kind].append(
                generate_course(item, nodes, prereqs)
            )

    # Return the node's name
    return name


def to_json(nodes, primary_node=''):
    """
    Transforms a set of nodes into json format
    Returns a tuple of jsonifiable dictionaries
    """

    transitions = []
    state_keys = {}

    for nodename in nodes:
        node = nodes[nodename]

        ###
        # Add State
        state_keys[nodename] = {'label': node['label']}

        # Categorize by type (intermediate/class)
        if (node['label'] == 'OR') or (node['label'] == 'AND'):
            state_keys[nodename]['type'] = 'intermediate'
        else:
            state_keys[nodename]['type'] = 'course'

            # Try to get the URL for the course
            # TODO: Currently Unused
            url = ''
            try:
                subject, number = nodename.split(' ')
                url = reverse('course_catalog.views.course_detail', kwargs={'subject_abbr': subject, 'course_number': number})
            except:
                pass

            state_keys[nodename]['url'] = url

        # Mark the primary node
        if nodename == primary_node:
            state_keys[nodename]['type'] += ' primary'

        ###
        # Add Transitions
        for link_type in ['prerequisite', 'recommend', 'corequisite']:
            if link_type in node:
                for connection in node[link_type]:
                    transitions.append({
                        'source': connection,
                        'target': nodename,
                        'type': link_type
                    })

    return transitions, state_keys


def to_dot(nodes):
    """
    Transforms a set of nodes into dotfile format
    Returns a string of the dotfile format
    """

    # Prefix
    outstr = '''digraph "Prerequisite Chart" {
    node [
        shape=ellipse,
        style=filled,
        fontname="'Droid Sans', sans-serif",
        color=forestgreen,
        fontcolor=white
    ]\n'''

    # Add the nodes
    for nodename in nodes:
        # Generate Nodes
        node = nodes[nodename]

        if (node['label'] == 'OR') or (node['label'] == 'AND'):
            outstr += '"%s" [ label="%s", title="%s", color="white", fontcolor="black" ]\n' % (nodename, node['label'], node['label'])
        else:
            url = ''

            try: # Try to get the URL for the course
                subject, number = nodename.split(' ')
                url = reverse('course_catalog.views.course_detail', kwargs={'subject_abbr': subject, 'course_number': number})
            except:
                pass

            outstr += '"%s" [ URL="%s" ]\n' % (nodename, url)

    # Add the links
    for nodename in nodes:
        # Generate links
        node = nodes[nodename]

        if 'prerequisite' in node:
            for connection in node['prerequisite']:
                outstr += '"%s" -> "%s"\n' % (connection, nodename)
        if 'recommend' in node:
            for connection in node['recommend']:
                outstr += '"%s" -> "%s" [ style="dotted" ]\n' % (connection, nodename)
        if 'corequisite' in node:
            for connection in node['corequisite']:
                outstr += '"%s" -> "%s" [ style="dashed" ]\n' % (connection, nodename)

    # Close the file out and return
    outstr += '}'
    return outstr
