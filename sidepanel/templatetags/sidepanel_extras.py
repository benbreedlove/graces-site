from django import template
from sidepanel.models import Sidepanel
from sidepanel import templatetags

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def show_sidepanels():
    panels = []
    for panel in Sidepanel.objects.all():
        panels.append(mark_safe(panel.content))

    return {'sidepanels':  panels}

register.inclusion_tag('includes/sidepanels.html')(show_sidepanels)
