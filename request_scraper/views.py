from django.http import HttpResponse
from request_scraper import test_request

from qcumber.config.private_config import SCRAPER_USERNAME, SCRAPER_PASSWORD

def index(request):

    return HttpResponse(test_request())
