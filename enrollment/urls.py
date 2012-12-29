from django.conf.urls import patterns, include, url

urlpatterns = patterns('enrollment.views',
    url(r'^(?P<subject_abbr>\w+)/(?P<course_num>\w+)/(?P<solus_id>\w+)/$', 'enrollment_numbers'),

)
