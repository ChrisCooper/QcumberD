# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('course_catalog.views',
    url(r'^$', 'index', name="home"),

    url(r'^catalog/(?P<subject_abbr>\w+)/(?P<course_number>\w+)/$', 'course_detail'),
    url(r'^catalog/(?P<subject_abbr>\w+)/$', 'subject_detail'),

    url(r'^search/$', 'search'),

    url(r'^about/$', 'about', name="about"),
    url(r'^contact/$', 'contact', name="contact"),
    url(r'^tos$', 'tos', name="tos"),
    url(r'^faqs$', 'faqs', name="faqs"),

    url(r'^robots.txt$', 'robots'),
    url(r'^crossdomain.xml$', 'flash_permissions'),
)
