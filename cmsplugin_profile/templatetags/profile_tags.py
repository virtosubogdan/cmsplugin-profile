import json
from django import template
from datetime import datetime


register = template.Library()

@register.assignment_tag
def current_timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
