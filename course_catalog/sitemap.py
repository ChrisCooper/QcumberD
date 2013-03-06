from django.contrib import sitemaps
from course_catalog.models import Course, Subject

class FlatpageSitemap(sitemaps.Sitemap):

    data = {"home": "/",
            "about": "/about",
            "contact": "/contact"}

    changefreq = "monthly"
    priority = 0.3

    def items(self): 
        return self.data.keys()

    def lastmod(self, obj):
        return None

    def location(self, obj):
        return self.data[obj]


class SubjectSitemap(sitemaps.Sitemap):
    
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Subject.objects.all()

    def lastmod(self, obj):
        return obj.last_encountered

class CourseSitemap(sitemaps.Sitemap):

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Course.objects.all()

    def lastmod(self, obj):
        return obj.last_encountered