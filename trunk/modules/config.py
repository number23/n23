import os
from google.appengine.ext import db

from theme import Theme, ThemeIterator

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

