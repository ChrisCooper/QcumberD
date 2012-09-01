from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from solus_scraper.Scraper import Scraper

def new_job(request):
    scraper = Scraper()
    scraper.full_scrape()
    return HttpResponse('Finished scrape pass')