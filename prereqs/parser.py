# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

#####################
# IMPORT STATEMENTS #
#####################


# Use ply to do the parsing
import ply.lex as lex
import ply.yacc as yacc

### USED FOR UTILS ###
import re


##################
# ENTERING UTILS #
##################


def re_insensitive(string):
    """
    Unfortunately, using the regex (?i) flag causes problems when
    other regexes don't want to be insensitive (like the t_COURSE regex)
    This is probably due to ply concatenating regexps
    Thus we need to use this hacky method.
    """
    outstring = ''
    for char in string:
        if re.match(r'[a-zA-Z]', char):
            outstring += '[' + char.upper() + char.lower() + ']'
        else:
            outstring += char
    return outstring


################
# ENTERING LEX #
################

###
# Define Tokens
###


tokens = (
    'COURSE',
    'RECOMMEND',
    'PREREQUISITE',
    'COREQUISITE',
    'EQUIVALENCY',
    'EXCLUSION',
    'OR',
    'LPAREN',
    'RPAREN',
)

###
# Define Token Rules
###


t_RECOMMEND = re_insensitive('recommend')
t_PREREQUISITE = re_insensitive('prerequisite')
t_COREQUISITE = re_insensitive('corequisite')
t_EQUIVALENCY = re_insensitive('equivalen')
t_EXCLUSION = re_insensitive('exclu')

t_OR = re_insensitive('or')

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_COURSE = r'[A-Z]{2,4}[ ]?[pP]?[0-9]{1,3}'


def t_error(t):
    # Skip any invalid characters
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


#################
# ENTERING YACC #
#################

###
# Parsing Rules
###


precedence = (
    ('right', 'OR'),
)


###
# Full document
###


def p_full(t):
    'full : reqsetlist'
    t[0] = t[1]


###
# REQSETLIST DEFINITIONS
###


def p_reqsetlist_empty(t):
    'reqsetlist : '
    t[0] = []


def p_reqsetlist_add(t):
    'reqsetlist : reqsetlist reqset'
    if len(t[2]['courses']['items']) is 0:
        t[0] = t[1]
    else:
        t[0] = t[1] + [t[2]]


###
# REQSET DEFINITIONS
###


def p_reqset_recommend(t):
    'reqset : RECOMMEND optcourselist'
    t[0] = {
        'type': 'recommend',
        'courses': t[2]
    }


def p_reqset_corequisite(t):
    'reqset : COREQUISITE optcourselist'
    t[0] = {
        'type': 'corequisite',
        'courses': t[2]
    }


def p_reqset_prerequisite(t):
    'reqset : PREREQUISITE optcourselist'
    t[0] = {
        'type': 'prerequisite',
        'courses': t[2]
    }


def p_reqset_equivalency(t):
    'reqset : EQUIVALENCY optcourselist'
    t[0] = {
        'type': 'equivalency',
        'courses': t[2]
    }


def p_reqset_exclusion(t):
    'reqset : EXCLUSION optcourselist'
    t[0] = {
        'type': 'exclusion',
        'courses': t[2]
    }


def p_reqset_bare(t):
    'reqset : courselist'
    # Default to prerequisites
    t[0] = {
        'type': 'prerequisite',
        'courses': t[1]
    }


###
# OPTIONAL COURSELIST
###


def p_optcourselist_full(t):
    'optcourselist : courselist'
    t[0] = t[1]


def p_optcourselist_empty(t):
    'optcourselist : '
    t[0] = {
        'type': 'and',
        'items': []
    }

###
# COURSELIST DEFINITIONS
###


def p_courselist_single(t):
    'courselist : COURSE'
    # Add a space at the correct location if it is missing
    course = t[1]
    if not (' ' in course):
        # Add a space immediately before the first digit in the string
        m = re.search('\d', course)
        if m:
            course = course[:m.start()] + ' ' + course[m.start():]

    t[0] = {
        'type': 'and',
        'items': [course]
    }


def p_courselist_noop(t):
    'courselist : courselist courselist'
    t[0] = courselist_and(t[1], t[2])


def p_courselist_or(t):
    'courselist : leftor courselist'
    t[0] = courselist_or(t[1], t[2])


def p_courselist_floatingor(t):
    'courselist : leftor'
    t[0] = t[1]


def p_courselist_parens(t):
    'courselist : LPAREN rightparen'
    # This simply ensures that the entire courselist inside 
    # of the parens has already been evaluated
    t[0] = t[2]


def p_courselist_emptyparens(t):
    'courselist : LPAREN RPAREN'
    t[0] = {
        'type': 'and',
        'items': []
    }


###
# OR
###


def p_rightparen(t):
    'rightparen : courselist RPAREN'
    t[0] = t[1]


def p_leftor(t):
    'leftor : courselist OR'
    t[0] = t[1]


def p_error(p):
    # Skipping bad tokens
    yacc.errok()

# Build the Parser
yacc.yacc()


####################
# ENTERING HELPERS #
####################


def courselist_and(a, b):
    if a['type'] is 'and' and b['type'] is 'and':
        return {
            'type': 'and',
            'items': a['items'] + b['items']
        }
    elif a['type'] is 'and' and b['type'] is 'or':
        return {
            'type': 'and',
            'items': a['items'] + [b]
        }
    elif a['type'] is 'or' and b['type'] is 'and':
        return {
            'type': 'and',
            'items': [a] + b['items']
        }
    else:
        return {
            'type': 'and',
            'items': [a, b]
        }


def courselist_or(a, b):
    if a['type'] is 'and' and b['type'] is 'and':
        # Collapse single element ands
        if len(a['items']) is 1:
            a = a['items'][0]
        if len(b['items']) is 1:
            b = b['items'][0]

        return {
            'type': 'or',
            'items': [a, b]
        }
    elif a['type'] is 'and' and b['type'] is 'or':
        # Collapse single element ands
        if len(a['items']) is 1:
            a = a['items'][0]

        return {
            'type': 'or',
            'items': [a] + b['items']
        }
    elif a['type'] is 'or' and b['type'] is 'and':
        # Collapse single element ands
        if len(b['items']) is 1:
            b = b['items'][0]

        return {
            'type': 'or',
            'items': a['items'] + [b]
        }
    else:
        return {
            'type': 'or',
            'items': a['items'] + b['items']
        }


####################
# ENTERING EXPORTS #
####################


def parse(string):
    """
    Parse the string passed in for prerequisites.
    Reformats the dictionary to be cleaner before returning
    (merges duplicate reqset types etc.)
    """
    reqsetlist = parse_raw(string)

    outdict = {}
    for reqset in reqsetlist:
        reqtype = reqset['type']
        if reqtype in outdict:
            # We have to merge them
            outdict[reqtype] = courselist_and(
                outdict[reqtype],
                reqset['courses']
            )
        else:
            outdict[reqtype] = reqset['courses']
    return outdict


def parse_raw(string):
    """
    Parse the string passed in for prerequisites.
    Returns the dictionary in the format generated by yacc
    """
    string = preprocess_string(string)
    return yacc.parse(string)


def preprocess_string(string):
    """
    Preprocesses the string, fixing any mismatched parens.
    If there is an unmatched ')', deletes it.
    If there is an unmatched '(', adds a ')' at the end to match it
    """

    depth = 0
    outstring = ''
    for char in string:
        if char == '(':
            depth += 1
        elif char == ')':
            if depth > 0:
                depth -= 1
            else:
                # Don't write out this character
                continue
        outstring += char
    if depth > 0:
        outstring += ')' * depth

    return outstring
