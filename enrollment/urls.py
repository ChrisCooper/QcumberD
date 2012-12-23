from django.conf.urls import patterns, include, url

urlpatterns = patterns('enrollment.views',
    url(r'^$', 'proof'),
)
