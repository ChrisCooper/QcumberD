# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',

    # Redirects from old URLs
    url(r'^courses/(?P<subject_abbr>\w+)_(?P<course_number>\w+)/$',
        "redirect_to", {"url": '/catalog/%(subject_abbr)s/%(course_number)s/', "permanent": True}),
    url(r'^subjects/(?P<subject_abbr>\w+)/$',
        'redirect_to', {"url": '/catalog/%(subject_abbr)s/', "permanent": True}),
    
    # Uncomment the next line to enable the SOLUS scraper
    url(r'^scraper/', include('scraper.urls')),

    # Uncomment the next line to enable checking of enrollment
    url(r'^enrollment/', include('enrollment.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('course_catalog.urls')),
)
