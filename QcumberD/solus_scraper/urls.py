from django.conf.urls import patterns, include, url

urlpatterns = patterns('solus_scraper.views',
    url(r'^new_job/$', 'new_job'),
)
