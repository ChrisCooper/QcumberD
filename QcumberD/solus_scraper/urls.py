from django.conf.urls import patterns, include, url

urlpatterns = patterns('solus_scraper.views',
    url(r'^$', 'index'),
    url(r'^new_job/(?P<config_name>.+)$', 'new_job'),
)
