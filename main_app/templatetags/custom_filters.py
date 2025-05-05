from django import template

register = template.Library()

@register.filter
def time_to_percent(value):
    """Convert a time to a top % for the calendar (without % symbol)."""
    if not value:
        return 0
    minutes = value.hour * 60 + value.minute
    return (minutes / (24 * 60)) * 100

@register.filter
def duration_to_percent(value):
    """Convert duration in minutes to height % (without % symbol)."""
    if not value:
        return 0
    return (value / (24 * 60)) * 100
