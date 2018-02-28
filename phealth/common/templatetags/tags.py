from django import template
import re


register = template.Library()

@register.filter(name='make_css')
def make_css(init_val):
	return re.sub(r' ', r'_', str(init_val))


@register.filter(name='datetime')
def filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format)
