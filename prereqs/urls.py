# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url

urlpatterns = patterns('prereqs.views',
    url(r'^$', 'index'),
    url(r'^parse/$', 'parse_all'),
    # url(r'^parse/(?P<subject_abbr>\w+)/$', 'parse_subject'),
    # url(r'^parse/(?P<subject_abbr>\w+)/(?P<course_number>\w+)/$', 'parse_course'),
)
