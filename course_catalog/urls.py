from django.conf.urls import patterns, include, url

urlpatterns = patterns('course_catalog.views',
    url(r'^$', 'index', name="home"),
    
    url(r'^courses/(?P<subject_abbr>\w+)_(?P<course_number>\w+)/$', 'course_detail'),
    url(r'^subjects/(?P<subject_abbr>\w+)/$', 'subject_detail'),
    url(r'^search/$', 'search'),


    url(r'^about/$', 'about', name="about"),
    url(r'^contact/$', 'contact', name="contact"),
    url(r'^tos$', 'tos', name="tos"),
    url(r'^faqs$', 'faqs', name="faqs"),

    url(r'^robots.txt$', 'robots'),
    url(r'^crossdomain.xml$', 'flash_permissions'),
)
