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

import cgi
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class PhoneBook(webapp.RequestHandler): 
    def get(self): 
        #user = users.get_current_user()
        #if user:
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write('Hello, webapp World!')
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.out.write('Hello, ' + user.nickname())
        #else:
        #    self.redirect(users.create_login_url(self.request_uri))

#        self.response.out.write('''
#            <html>
#              <body>
#                <form action="/sign" method="post">
#                  <div><textarea name="content" rows="3" cols="60"/></textarea>
#                  </div>
#                  <div><input type="submit" value="Sign Guestbook"></div>
#                </form>
#              </body>
#            </html>''')

        self.response.out.write('''
                <form action="/sign" method="post">
                  <div><textarea name="content" rows="3" cols="60"/></textarea>
                  </div>
                  <div><input type="submit" value="Sign Guestbook"></div>
                </form>
              </body>
            </html>''')

def main(): 
    application = webapp.WSGIApplication(
                                       [('/phoneBook/', PhoneBook)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
