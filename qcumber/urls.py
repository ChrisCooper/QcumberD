# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, include, url
from course_catalog.sitemap import *

sitemaps = {
    'flatpages': FlatpageSitemap,
    'subjects': SubjectSitemap,
    'courses': CourseSitemap
}

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the next line to enable the SOLUS scraper
    url(r'^scraper/', include('scraper.urls')),

    # Uncomment the next line to enable the exambank scraper
    url(r'^exams/', include('exams.urls')),

    # Uncomment the next line to enable the textboook scraper
    url(r'^textbooks/', include('textbooks.urls')),

    # Uncomment the next line to enable checking of enrollment
    url(r'^enrollment/', include('enrollment.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {"sitemaps": sitemaps}),

    url(r'^', include('course_catalog.urls')),

    # Redirects from old URLs
    url(r'^', include('moved_pages.urls')),
)
