# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from course_catalog.model_controls import clear_old_models

from scraper.models import JobConfig
from scraper.catalog_scraper import CatalogScraper
import os
import json
from course_catalog.models import existing_or_new, Subject, Course, Career, \
    GradingBasis, Consent, Section, SectionType, SectionComponent, Term, \
    Season, Instructor, Timeslot, DayOfWeek

@staff_member_required
def index(request):
    """Lists all the job configurations"""
    job_configs = JobConfig.objects.all()

    return render(request, 'scraper/index.html', {'job_configs' : job_configs})

@staff_member_required
def new_job(request, config_name):
    """Starts a new scraping job"""

    config = get_object_or_404(JobConfig, name=config_name)

    start_time = datetime.datetime.now()

    try:
        s = CatalogScraper(config=config)
        s.scrape_all()
    except Exception:
        print ("Error during scraping (time taken: " + str(datetime.datetime.now() - start_time) + ")")
        raise

    deleted = None
    if config.delete_other_models:
        deleted = clear_old_models(start_time)

    # Make a pretty time taken string
    seconds = (datetime.datetime.now() - start_time).seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_taken = '{0} hours, {1} minutes, {2} seconds.'.format(hours, minutes, seconds)

    # Don't want django model stuff to show up
    del config._state

    return render(request, 'scraper/scrape_result.html', {'time_taken' : time_taken, 'config': config.__dict__, 'deleted': deleted})

@staff_member_required
def load_json_dump(request):
    print "starting data load"
    start_time = datetime.datetime.now()

    log = []
    if 'qcumber-data' in os.listdir('.'):
        log.append('qcumber-data dir found')
        data_parts = os.listdir('./qcumber-data')

        if 'subjects' in data_parts:
            log.append('parsing subject data')
            for file_name in os.listdir('./qcumber-data/subjects'):
                if file_name.endswith('.json'):
                    with open('./qcumber-data/subjects/'+file_name, 'r') as f:
                        json_to_subject(f.read())
            log.append('finished loading subjects!')

        else:
            log.append('no subjects data')

        if 'courses' in data_parts:
            log.append('parsing courses data')
            for file_name in os.listdir('./qcumber-data/courses'):
                if file_name.endswith('.json'):
                    with open('./qcumber-data/courses/'+file_name, 'r') as f:
                        json_to_course(f.read())
            log.append('finished loading courses!')

        else:
            log.append('no courses data')

        if 'sections' in data_parts:
            log.append('parsing section data')
            for file_name in os.listdir('./qcumber-data/sections'):
                if file_name.endswith('.json'):
                    with open('./qcumber-data/sections/'+file_name, 'r') as f:
                        json_to_section(f.read())
            log.append('finished loading sections!')

        else:
            log.append('no sections data')

    else:
        log.append('qcumber-data dir not found')

    # Make a pretty time taken string
    seconds = (datetime.datetime.now() - start_time).seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_taken = '{0} hours, {1} minutes, {2} seconds.'.format(hours, minutes, seconds)
    print "finished data load, took %s" % time_taken

    return render(request, 'scraper/json_load.html', {'log' : log})

def json_to_subject(file_contents):
    raw = json.loads(file_contents)
    existing_or_new(Subject, **{
        'title': raw['title'],
        'abbreviation': raw['abbreviation']
    })

def json_to_course(file_contents):
    temp = json.loads(file_contents)
    raw = temp['basic']
    if 'extra' in temp:
        raw.update(temp['extra'])

    course_dict = {}
    # The actuall course
    course_map = {
        'title': 'title',
        'description': 'description',
        'number': 'number',
        'units': 'units',
        'enrollment_reqs': 'enrollment_requirement'
    }

    for key in course_map:
        if course_map[key] in raw:
            course_dict[key] = raw[course_map[key]]

    # Subject
    course_dict['subject'] = existing_or_new(Subject, **{
        'abbreviation': raw['subject']})

    # Career
    if 'career' in raw:
        course_dict['career'] = existing_or_new(Career, **{
            'name': raw['career']})

    # Grading
    if 'grading_basis' in raw:
        course_dict['grading_basis'] = existing_or_new(GradingBasis, **{
            'name': raw['grading_basis']})

    # Consent
    if 'add_consent' in raw:
        consent = existing_or_new(Consent, **{'name': raw['add_consent']})

    if 'drop_consent' in raw:
        course_dict['drop_consent'] = existing_or_new(Consent, **{
            'name': raw['drop_consent']})

    existing_or_new(Course, **course_dict)

def json_to_section(file_contents):
    raw = json.loads(file_contents)
    basic = raw['basic']

    section_dict = {
        'solus_id': basic['class_num'],
        'index_in_course': basic['solus_id']
    }

    # Course
        #Subject
    subject = existing_or_new(Subject, **{'abbreviation': basic['subject']})
    section_dict['course'] = existing_or_new(Course, **{
        'subject': subject,
        'number': basic['course']
    })

    # SectionType
    section_dict['type'] = existing_or_new(SectionType, **{
        'abbreviation':basic['type']})


    # Term
        # Season
    season = existing_or_new(Season, **{'name':basic['season']})
    section_dict['term'] = existing_or_new(Term, **{
        'season': season,
        'year': basic['year']
    })

    section = existing_or_new(Section, **section_dict)

    # SectionComponent
    for raw_class in raw['classes']:
        sec_comp_dict = {
            'start_date': datetime.datetime.strptime(raw_class['term_start'], "%Y-%m-%dT%H:%M:%S"),
            'end_date': datetime.datetime.strptime(raw_class['term_end'], "%Y-%m-%dT%H:%M:%S"),
            'room': raw_class['location'],
            'section': section
        }

        # Timeslot
        if raw_class['start_time'] is None \
            or raw_class['end_time'] is None \
            or raw_class['day_of_week'] is None:
            sec_comp_dict['timeslot'] = None
        else:
            sec_comp_dict['timeslot'] = existing_or_new(Timeslot, **{
                'start_time': datetime.datetime.strptime(raw_class['start_time'], "%Y-%m-%dT%H:%M:%S"),
                'end_time': datetime.datetime.strptime(raw_class['end_time'], "%Y-%m-%dT%H:%M:%S"),
                'day_of_week': existing_or_new(DayOfWeek, **{'abbreviation': iso_day_to_abrev[raw_class['day_of_week']]})
            })

        section_component = existing_or_new(SectionComponent, **sec_comp_dict)

        # can't add instructors at object creation time
        instructors = []
        for prof in raw_class['instructors']:
            instructors.append(existing_or_new(Instructor, **{
                'name': prof}))
        setattr(section_component, 'instructors', instructors)
        section_component.save()

iso_day_to_abrev = {
    1: 'Mo',
    2: 'Tu',
    3: 'We',
    4: 'Th',
    5: 'Fr',
    6: 'Sa',
    7: 'Su'
}
