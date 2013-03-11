# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',

	url(r'^signup/$',  TemplateView.as_view(template_name='registration/signup.html'), name='signup'),

	url(r'^login/$',  login, name='login'),
	url(r'^logout/$', logout, name='logout'),
)
