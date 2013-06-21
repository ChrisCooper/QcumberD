# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.http import HttpResponse
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('course_catalog.views',
    url(r'^$', 'index', name="home"),

    url(r'^catalog/(?P<subject_abbr>\w+)/(?P<course_number>\w+)/$', 'course_detail'),
    url(r'^catalog/(?P<subject_abbr>\w+)/$', 'subject_detail'),

    url(r'^search/$', 'search'),
)

urlpatterns += patterns('',

    # Static templates
    url(r'^about/$', TemplateView.as_view(template_name='course_catalog/text/about.html'), name="about"),
    url(r'^contact/$',  TemplateView.as_view(template_name='course_catalog/text/contact.html'), name="contact"),
    url(r'^tos$', TemplateView.as_view(template_name='course_catalog/text/tos.html'), name="tos"),
    url(r'^faqs$', TemplateView.as_view(template_name='course_catalog/text/faqs.html'), name="faqs"),
    url(r'^resources$', TemplateView.as_view(template_name='course_catalog/text/resources.html'), name="resources"),

    url(r'^robots.txt$', TemplateView.as_view(template_name='course_catalog/text/faqs.html')),
    url(r'^crossdomain.xml$', lambda r: HttpResponse('')),
)
