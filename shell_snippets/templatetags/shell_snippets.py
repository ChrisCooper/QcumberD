from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def admin_edit_url(object, action='change'):
	'''Returns the url to the supplied object in the admin interface.'''
	return reverse('admin:%s_%s_change' %(object._meta.app_label,  object._meta.module_name),  args=[object.id] )

#@register.filter
def shell_snippet_dropdown(object):
    pass