#! /usr/bin/env python

#print 'Content-Type: text/plain'
#print ''
#print 'Hello, world!'

import cgi
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler): 
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

        self.response.out.write('<html><body>')
        greetings = db.GqlQuery('SELECT * FROM Greeting ORDER BY date DESC LIMIT 10')
        for greeting in greetings:
            if greeting.author:
                self.response.out.write('<b>%s</b> wrote: ' % greeting.author.nickname())
            else:
                self.response.out.write('An anonymous person wrote:')
            self.response.out.write('<blockquote> %s </blockquote>' %
                                    cgi.escape(greeting.content))
        self.response.out.write('''
                <form action="/sign" method="post">
                  <div><textarea name="content" rows="3" cols="60"/></textarea>
                  </div>
                  <div><input type="submit" value="Sign Guestbook"></div>
                </form>
              </body>
            </html>''')

class Guestbook(webapp.RequestHandler):
    def post(self):
        #self.response.out.write('<html><body>You wrote:<pre>')
        #self.response.out.write(cgi.escape(self.request.get('content')))
        #self.response.out.write('</pre></body></html>')
        greeting = Greeting()
        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

def main(): 
    application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        ('/sign', Guestbook)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
