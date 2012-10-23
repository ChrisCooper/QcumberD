from django.conf.urls import patterns, include, url

urlpatterns = patterns('course_catalog.views',
    url(r'^$', 'index', name="home"),
    url(r'^course/(?P<subject_abbr>\w+)_(?P<course_number>\w+)/$', 'course_detail'),
    url(r'^subject/(?P<subject_abbr>\w+)/$', 'subject_detail'),
    url(r'^search/$', 'search'),
    url(r'^experiments$', 'experiments'),
)
