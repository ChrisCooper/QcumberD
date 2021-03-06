# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from textbooks.models import JobConfig
from textbooks.textbook_scraper import TextbookScraper

@staff_member_required
def index(request):
    """Lists all the job configurations"""
    job_configs = JobConfig.objects.all()

    return render(request, 'textbooks/index.html', {'job_configs' : job_configs})

@staff_member_required
def new_job(request, config_name):
    """Starts a new scraping job"""
    config = get_object_or_404(JobConfig, name=config_name)

    t = datetime.datetime.now()

    try:
        TextbookScraper(config).scrape()
        return HttpResponse("Finished scrape pass (time taken: " + str(datetime.datetime.now() - t) + ")")
    except Exception:
        print ("Error during scraping (time taken: " + str(datetime.datetime.now() - t) + ")")
        raise