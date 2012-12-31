# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

from request_scraper.models import JobConfig
from request_scraper.solus_data import update_constants
from request_scraper.solus_scraper import SolusScraper


def index(request):
    """Lists all the job configurations"""
    job_configs = JobConfig.objects.all()

    return render_to_response('request_scraper/index.html', {'job_configs' : job_configs})

def new_job(request, config_name):
    """Starts a new scraping job"""
    config = get_object_or_404(JobConfig, name=config_name)

#try:
    SolusScraper(config, SCRAPER_USERNAME, SCRAPER_PASSWORD).scrape_all()
    return HttpResponse('Finished scrape pass')
#except Exception as e:
    #return HttpResponse("Something went wrong:<br/>" + str(e))
#    raise e

def constants(request):

    update_constants()

    return HttpResponse('Constants updated')