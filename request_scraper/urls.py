from django.conf.urls import patterns, include, url

urlpatterns = patterns('request_scraper.views',
    url(r'^$', 'index'),
)
