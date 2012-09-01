from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from solus_scraper.models import JobConfig
from solus_scraper.scraper import SolusScraper

def new_job(request, config_name):
    config = get_object_or_404(JobConfig, name=config_name)

    scraper = SolusScraper()
    scraper.full_scrape(config)

    return HttpResponse('Finished scrape pass')