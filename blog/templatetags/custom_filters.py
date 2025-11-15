# blog/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    """Check if a string ends with the given suffix"""
    if not isinstance(value, str):
        value = str(value)
    return value.lower().endswith(str(suffix).lower())
