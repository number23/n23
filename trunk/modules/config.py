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


from google.appengine.ext import db

from theme import Theme

__all__ = [
        'Config',
        'config',
        'global_vars',
        ]

global_vars = {}


class Config(db.Expando):
    blog_title = db.StringProperty(default = 'Blog')
    blog_subtitle = db.StringProperty(default = '')
    posts_per_page = db.IntegerProperty(default = 10)
    comments_per_page = db.IntegerProperty(default = 10)
    recent_posts = db.IntegerProperty(default = 5)
    recent_comments = db.IntegerProperty(default = 5)
    rss_posts = db.IntegerProperty(default = 10)
    default_host = db.StringProperty(default = '')
    site_keywords = db.StringProperty(default = '')
    site_description = db.StringProperty(default = '')
    theme = db.StringProperty(required = True, default = 'default')
    custom_header = db.TextProperty(default = '')
    custom_sidebar = db.TextProperty(default = '')
    custom_footer = db.TextProperty(default = '')
    last_config_time = db.DateTimeProperty()

config = Config.get_by_key_name('default')
if not config:
    config = Config(key_name = 'default')

key = config.put()

if not config.default_host:
    config.default_host = 'http://%s.appspot.com' % key.app().encode('utf-8')
    config.put()

global_vars['theme'] = Theme(config.theme)
