from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from solus_scraper.models import JobConfig
from solus_scraper.scraper import full_scrape

def index(request):
    job_configs = JobConfig.objects.all()

    return render_to_response('solus_scraper/index.html', {'job_configs' : job_configs})

def new_job(request, config_name):
    config = get_object_or_404(JobConfig, name=config_name)

    full_scrape(config)

    return HttpResponse('Finished scrape pass')