# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from exams.models import JobConfig
from exams.exam_scraper import ExamScraper

@staff_member_required
def index(request):
    """Lists all the job configurations"""
    job_configs = JobConfig.objects.all()

    return render(request, 'exams/index.html', {'job_configs' : job_configs})

@staff_member_required
def new_job(request, config_name):
    """Starts a new exam scraping job"""

    config = get_object_or_404(JobConfig, name=config_name)

    start_time = datetime.datetime.now()

    try:
        s = ExamScraper(config=config).scrape()
    except Exception:
        print ("Error during scraping (time taken: " + str(datetime.datetime.now() - start_time) + ")")
        raise

    # Make a pretty time taken string
    seconds = (datetime.datetime.now() - start_time).seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_taken = '{0} hours, {1} minutes, {2} seconds.'.format(hours, minutes, seconds)

    # Don't want django model stuff to show up
    del config._state

    return render(request, 'exams/scrape_result.html', {'time_taken' : time_taken, 'config': config.__dict__})