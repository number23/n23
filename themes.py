import os
import sys
import logging
import wsgiref.handlers
from mimetypes import types_map
from datetime import datetime, timedelta
from google.appengine.ext import webapp

sys.path.append('modules')
from config import config

cwd = os.getcwd()
theme_path = os.path.join(cwd, 'themes')

max_age = 600  #expires in 10 minutes

class GetFile(webapp.RequestHandler):
    def get(self):
        request_path = self.request.path[8:]
        server_path = os.path.normpath(os.path.join(cwd, 'themes', request_path))

        if self.request.if_modified_since and self.request.if_modified_since.replace(tzinfo=None) >= config.last_config_time:
            self.response.headers['Date'] = format_date(datetime.utcnow())
            self.response.headers['Last-Modified'] = format_date(config.last_config_time)
            cache_expires(self.response, max_age)
            self.response.set_status(304)
            self.response.clear()

        elif server_path.startswith(theme_path):
            ext = os.path.splitext(server_path)[1]
            if types_map.has_key(ext):
                mime_type = types_map[ext]
            else:
                mime_type = 'application/octet-stream'
            try:
                self.response.headers['Content-Type'] = mime_type
                self.response.headers['Last-Modified'] = format_date(config.last_config_time)
                cache_expires(self.response, max_age)
                self.response.out.write(open(server_path, 'rb').read())
            except Exception, e:
                logging.info(e)
                self.redirect('/static/pages/404.html')
        else:
            self.redirect('/static/pages/404.html')

class NotFound(webapp.RequestHandler):
    def get(self):
        logging.info(self.request.path)
        self.redirect('/static/pages/404.html')

def format_date(dt):
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

def cache_expires(response, seconds=0, **kw):
    """
    Set expiration on this request.  This sets the response to
    expire in the given seconds, and any other attributes are used
    for cache_control (e.g., private=True, etc).

    this function is modified from webob.Response
    it will be good if google.appengine.ext.webapp.Response inherits from this class...
    """
    if not seconds:
        # To really expire something, you have to force a
        # bunch of these cache control attributes, and IE may
        # not pay attention to those still so we also set
        # Expires.
        response.headers['Cache-Control'] = 'max-age=0, must-revalidate, no-cache, no-store'
        response.headers['Expires'] = format_date(datetime.utcnow())
        if 'last-modified' not in self.headers:
            self.last_modified = format_date(datetime.utcnow())
        response.headers['Pragma'] = 'no-cache'
    else:
        response.headers['Cache-Control'] = 'max-age=%d' % seconds
        response.headers['Expires'] = format_date(datetime.utcnow() + timedelta(seconds=seconds))

def main():
    application = webapp.WSGIApplication(
            [
                ('/themes/[\\w\\-]+/templates/.*', NotFound),
                ('/themes/[\\w\\-]+/.+', GetFile),
                ('.*', NotFound),
                ],
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

