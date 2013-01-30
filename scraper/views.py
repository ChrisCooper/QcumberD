# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

from course_catalog.model_controls import clear_old_models

from scraper.models import JobConfig
from scraper.solus_scraper import SolusScraper


def index(request):
    """Lists all the job configurations"""
    job_configs = JobConfig.objects.all()

    return render(request, 'scraper/index.html', {'job_configs' : job_configs})

def new_job(request, config_name):
    """Starts a new scraping job"""
    
    config = get_object_or_404(JobConfig, name=config_name)

    start_time = datetime.datetime.now()

    try:
        SolusScraper(config, SCRAPER_USERNAME, SCRAPER_PASSWORD).scrape_all()
    except Exception:
        print ("Error during scraping (time taken: " + str(datetime.datetime.now() - start_time) + ")")
        raise


    if config.delete_other_models:
        clear_old_models(start_time)

    return HttpResponse("Finished scrape pass (time taken: " + str(datetime.datetime.now() - start_time) + ")")