#! /usr/bin/env python

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

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):

    def get(self):
        img_list = os.listdir('static/images/OpenBSD')
        img_data = 'var rotateDATA = [\n'
        for img in img_list:
            if img == '.svn': continue
            img_data += '{imgSRC : "/static/images/OpenBSD/%s"},\n' % img
        img_data = img_data[:-2] + '];\n'
        template_values = {'img_data': img_data}

        path = os.path.join(os.path.dirname(__file__), 'static/pages/index.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication(
                                       [('/', MainPage)],
                                       debug=False)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
