# templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def has_event(event_dict, day):
    if day in event_dict.keys():
        print(event_dict[day][0])
        return event_dict[day][0]
    else:
        return None