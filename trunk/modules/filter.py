from django import template
from datetime import timedelta


__all__ = ['register', 'default_filter']

register = template.Library()


def timezone(value, offset):
    return value + timedelta(hours=offset)


register.filter(timezone)
from html_filter import html_filter

blog_filter = html_filter()
blog_filter.allowed = {
        'a': ('href', 'target', 'name'),
        'b': (),
        'blockquote': (),
        'pre': (),
        'em': (),
        'i': (),
        'img': ('src', 'width', 'height', 'alt', 'title'),
        'strong': (),
        'u': (),
        'font': ('color', 'size'),
        'p': (),
        'h1': (),
        'h2': (),
        'h3': (),
        'h4': (),
        'h5': (),
        'h6': (),
        'table': (),
        'tr': (),
        'th': (),
        'td': (),
        'ul': (),
        'ol': (),
        'li': (),
        'br': (),
        'hr': (),
        }

blog_filter.no_close += ('br', )
blog_filter.allowed_entities += ('nbsp', 'ldquo', 'rdquo', 'hellip')
blog_filter.make_clickable_urls = False
# enable this will get a bug about a and img

default_filter = blog_filter.go
