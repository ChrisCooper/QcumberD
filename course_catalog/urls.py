# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('course_catalog.views',
    url(r'^$', 'index', name="home"),

    url(r'^catalog/(?P<subject_abbr>\w+)/(?P<course_number>\w+)/$', 'course_detail'),
    url(r'^catalog/(?P<subject_abbr>\w+)/$', 'subject_detail'),

    url(r'^search/$', 'search'),
)

urlpatterns += patterns('django.views.generic.simple',

    # Static templates
    url(r'^about/$', 'direct_to_template', {'template': 'course_catalog/text/about.html'}, name="about"),
    url(r'^contact/$',  'direct_to_template', {'template': 'course_catalog/text/contact.html'}, name="contact"),
    url(r'^tos$', 'direct_to_template', {'template': 'course_catalog/text/tos.html'}, name="tos"),
    url(r'^faqs$', 'direct_to_template', {'template': 'course_catalog/text/faqs.html'}, name="faqs"),

    url(r'^robots.txt$', 'direct_to_template', {'template': 'course_catalog/text/faqs.html'}),
    url(r'^crossdomain.xml$', lambda r: HttpResponse('')),
)
