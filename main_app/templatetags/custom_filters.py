from django import template

register = template.Library()

@register.filter
def time_to_percent(value):
    """Convert a time to a top % for the calendar."""
    if not value:
        return "0%"
    minutes = value.hour * 60 + value.minute
    percent = (minutes / (24 * 60)) * 100
    return f"{percent}%"

@register.filter
def duration_to_percent(value):
    """Convert a duration (in minutes) to a height % for the calendar."""
    if not value:
        return "0%"
    percent = (value / (24 * 60)) * 100
    return f"{percent}%"
