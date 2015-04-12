from django import template
from ninformes import settings

register = template.Library()

@register.simple_tag
def site_name():
    return settings.SITE_NAME

@register.simple_tag
def short_site_name():
    return settings.SHORT_SITE_NAME
