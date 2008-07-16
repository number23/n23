# Copyright 2008 N23 <No.0023@gmail.com>
# All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# $Id$

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
