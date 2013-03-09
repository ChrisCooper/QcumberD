# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns('',

    url(r'^courses/(?P<subject_abbr>\w+)_(?P<course_number>\w+)/$',
		RedirectView.as_view(url='/catalog/{subject_abbr}/{course_number}/')
	),
    url(r'^subjects/(?P<subject_abbr>\w+)/$',
        RedirectView.as_view(url='/catalog/{subject_abbr}/'),
    ),
    url(r'^catalog/$',
        RedirectView.as_view(url='/', permanent=False),
    ),

)
