import parser
import csv
import uuid

def generate_subject(subject, subjects):
    courses = subjects[subject]

    nodes = {}

    for coursenum in courses:
        coursename = '%s %s' % (subject, coursenum)
        if not coursenum[0] in ['6', '7', '8', '9']:
            generate_course(coursename, nodes, subjects)

    return nodes


def generate_course(coursename, nodes, subjects):
    if coursename in nodes:
        return coursename # You have already been generated

    nodes[coursename] = {'label': coursename}

    if coursename.find(' ') is -1:
        # There is no space!
        return coursename

    subject, coursenum = coursename.split(' ')
    if not (subject in subjects and coursenum in subjects[subject]):
        # Don't bother with prerequisites
        return coursename

    course = subjects[subject][coursenum]

    types = ['prerequisite', 'corequisite', 'recommend']
    for kind in types:
        if kind in course:
            node = course[kind]
            if node['type'] == 'or':
                node = {
                    'type': 'and',
                    'items': [node]
                }
            generate_node(node, kind, nodes, subjects, coursename)

    return coursename


def generate_node(source, kind, nodes, subjects, name=None):
    """
    SOURCE: {'type': 'or/and', 'items': []}
    NAME: 'CISC 101 or 1or'
    KIND: 'prerequisite/corequisite/recommend'
    NODES: node object
    SUBJECTS: subject object
    """
    if name is None:
        name = str(uuid.uuid4())
        label = source['type'].upper()
    else:
        label = name

    if not name in nodes:
        # We have not already generated that node
        nodes[name] = {
            kind: [],
            'label': label
        }
    else:
        nodes[name][kind] = []

    for item in source['items']:
        if type(item) is dict:
            # This is an and/or - recurse
            nodes[name][kind].append(
                generate_node(item, kind, nodes, subjects)
            )
        else:
            # This is a course
            nodes[name][kind].append(item)
            generate_course(item, nodes, subjects)

    return name


def to_dot(nodes):
    outstr = '''digraph G {
    node [
        shape=ellipse,
        style=filled,
        color=lightgreen
    ]'''
    for nodename in nodes:
        # Generate Nodes
        node = nodes[nodename]

        print node['label'], node['label'] == 'AND', node['label'] == 'OR',
        if (node['label'] == 'OR') or (node['label'] == 'AND'):
            color = 'white'
        else:
            color = 'lightgreen'

        print color

        outstr += '"%s" [ label="%s", color="%s" ]\n' % (nodename, node['label'], color)

    for nodename in nodes:
        # Generate links
        node = nodes[nodename]

        if 'prerequisite' in node:
            for connection in node['prerequisite']:
                outstr += '"%s" -> "%s"\n' % (connection, nodename)
        # if 'recommend' in node:
        #     for connection in node['recommend']:
        #         outstr += '"%s" -> "%s" [ style="dotted" ]\n' % (connection, nodename)
        if 'corequisite' in node:
            for connection in node['corequisite']:
                outstr += '"%s" -> "%s" [ style="dashed" ]\n' % (connection, nodename)

    outstr += '}'
    return outstr


if __name__ == '__main__':
    subjects = {}

    with open('output-stripped.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0].strip()
            subject, coursenum = name.split()
            print 'parsing for %s' % name

            requirements = row[1].strip()
            parsed = parser.parse(requirements)

            if not subject in subjects:
                subjects[subject] = {}

            subjects[subject][coursenum] = parsed

    with open('out.html', 'w') as htmlfile:
        htmlfile.write('''<!DOCTYPE html><html><head></head><body>\n''')

        for subject in subjects:
            generated = generate_subject(subject, subjects)
            htmlfile.write('<script type="text/vnd.graphviz" id="%s">\n' % subject)
            htmlfile.write(to_dot(generated))
            htmlfile.write('\n</script>\n')

        htmlfile.write('<script src="viz.js"></script>\n')
        htmlfile.write('''<script>
            function src(id) {return document.getElementById(id).innerHTML;}
            function display(id) {
                var result;
                try {
                    return Viz(src(id), "svg")
                } catch(e) {
                    return e.toString();
                }
            }\n''')

        for subject in subjects:
            if subject != 'CHEM':
                htmlfile.write('/*')
            htmlfile.write('document.body.innerHTML += "<h1>%s</h1>";\n' % subject)
            htmlfile.write('document.body.innerHTML += display("%s");\n' % subject)
            if subject != 'CHEM':
                htmlfile.write('*/')

        htmlfile.write('</script></body></html>')

