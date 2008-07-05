#! /usr/bin/env python

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):

    def get(self):
        template_values = {}

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication(
                                       [('/', MainPage)],
                                       debug=False)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
