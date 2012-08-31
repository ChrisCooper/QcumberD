from django.conf.urls import patterns, include, url

urlpatterns = patterns('course_catalog.views',
    url(r'^$', 'index'),
    url(r'^course/(?P<course_id>\d+)/$', 'course_detail'),
)
