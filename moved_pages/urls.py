# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('django.views.generic.simple',

    url(r'^courses/(?P<subject_abbr>\w+)_(?P<course_number>\w+)/$', "redirect_to",
        {"url": '/catalog/%(subject_abbr)s/%(course_number)s/', "permanent": True}),
    url(r'^subjects/(?P<subject_abbr>\w+)/$', 'redirect_to',
        {"url": '/catalog/%(subject_abbr)s/', "permanent": True}),
    url(r'^catalog/$', 'redirect_to',
        {"url": '/', "permanent": False}),

)
