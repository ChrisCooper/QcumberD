# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('textbooks.views',
    url(r'^$', 'index'),
    url(r'^new_job/(?P<config_name>.+)$', 'new_job'),
)
