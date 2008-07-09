import re
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from config import global_vars, config
from models import User, Post, Admin, AccessLogger, Comment, Tag
from filter import default_filter
from theme import Theme
import widget


class BaseRequestHandler(webapp.RequestHandler):

    def __init__(self):
        pass

    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)

        self.login_user = users.get_current_user()
        self.is_login = (self.login_user != None)
        if self.is_login:
            self.user = User.all().filter('user = ',
                                          self.login_user).get() or \
                        User(user = self.login_user)
        else:
            self.user = None
        # Access Logger
        #self.log()

        self.is_admin = users.is_current_user_admin()
        self.widget = Widget(self)
        self.theme = global_vars['theme']

        try:
            self.referer = self.request.headers['referer']
        except:
            self.referer = None

        self.template_values = {
                'self': self,
                'config': config,
                'theme': self.theme,
                'W': self.widget,
                }

    def param(self, name, **kw):
        return self.request.get(name, **kw)

    def write(self, s):
        self.response.out.write(s)

    def render(self, name, values=None):
        if values == None:
            values = self.template_values
        try:
            self.response.out.write(template.render(name, values))
        except:
            global_vars['theme'] = Theme()
            self.redirect('/blog/')

    def get_login_url(self, from_referer=False):
        if from_referer:
            dst = self.referer
            if not dst:
                dst = '/blog/'
            return users.create_login_url(dst)
        else:
            return users.create_login_url(self.request.uri)

    def get_logout_url(self, from_referer=False):
        if from_referer:
            dst = self.referer
            if not dst:
                dst = '/blog/'
            return users.create_logout_url(dst)
        else:
            return users.create_logout_url(self.request.uri)

    def chk_login(self, redirect_url='/blog/'):
        if self.is_login:
            return True
        else:
            self.redirect(redirect_url)
            return False

    def chk_admin(self, redirect_url='/blog/'):
        if self.is_admin:
            return True
        else:
            self.redirect(redirect_url)
            return False

    def log(self):
        al = AccessLogger(
                user = users.get_current_user(),
                remoteAddr = self.request.remote_addr,
                queryPath = self.request.path)
        al.put()


class Widget:

    def __init__(self, handler):
        self.handler = handler

    def __getitem__(self, name):
        try:
            name = name.lower()
            widget_generator = getattr(widget, name)
            html = widget_generator(self.handler.template_values)

            if html:
                return html
            else:
                return ''
        except Exception, e:
            return e


def new_post(title, content,
             author = users.get_current_user(), tags = [],
             date = None, filter = default_filter):
    if filter:
        content = filter(content)

    if date == None:
        post = Post(
                title = title,
                content = content,
                author = author,
                tags = tags,
                )
    else:
        post = Post(
                title = title,
                content = content,
                author = author,
                tags = tags,
                date = date)
    key = post.put()

    update_tag_count(old_tags = [], new_tags = tags)

    return key.id()


def edit_post(postid, title = None, content = None,
              author = users.get_current_user(), tags = None,
              date = None, filter = default_filter):
    if filter:
        content = filter(content)

    post = Post.get_by_id(int(postid))
    if title:
        post.title = title
    if content:
        post.content = content
    if author:
        post.last_modify_by = author
    if date:
        post.last_modify_date = date
    if tags != None:
        old_tags = post.tags
        post.tags = tags

    post.put()

    if tags != None:
        update_tag_count(old_tags = old_tags, new_tags = tags)


def delete_post(postid):
    post = Post.get_by_id(int(postid))
    if not post:
        return

    comments = Comment.all().filter('post = ', post)
    for comment in comments:
        comment.delete()

    post.delete()
    update_tag_count(old_tags = post.tags, new_tags = [])


def split_tags(s):
    tags = list(set([t.strip() for t in re.split('[,;\\/\\\\]*',\
                s) if t != ''])) #uniq
    return tags


def update_tag_count(old_tags = None, new_tags = None):
    if old_tags == None and new_tags == None:
        tags = []
        posts = Post.all()
        for post in posts:
            tags += post.tags
        tags_set = set(tags)
        for tag in tags_set:
            t = Tag.all().filter('name = ', tag).get()
            if t:
                t.count = tags.count(tag)
            else:
                t = Tag(name = tag, count = tags.count(tag))

            t.put()

    else:
        added = [t for t in new_tags if not t in old_tags]
        deleted = [t for t in old_tags if not t in new_tags]

        for tag in added:
            t = Tag.all().filter('name = ', tag).get()
            if t:
                t.count = t.count + 1
            else:
                t = Tag(name = tag, count = 1)

            t.put()

        for tag in deleted:
            t = Tag.all().filter('name = ', tag).get()
            if t:
                t.count = t.count - 1
                if t.count == 0:
                    t.delete()
                else:
                    t.put()
            else:
                t = Tag(name = tag, count = 1)
                t.put()


def regenerate_password(user):
    '''
    Generate a random string for using as api password,
    api user is user's full email
    '''
    from random import sample
    from md5 import md5
    s = 'abcdefghijklmnopqrstuvwxyz1234567890'
    password = ''.join(sample(s, 8))
    admin = Admin.all().filter('user = ', user).get()
    if not admin:
        admin = Admin(user = user)
    admin.api_password = md5(user.email() + 'blog' + password).hexdigest()
    admin.put()
    return password


def check_api_user_pass(email, password):
    from md5 import md5

    user = users.User(email)
    admin = Admin.all().filter('user = ', user).get()

    if not admin:
        return None

    if admin.api_password == md5(user.email() + 'blog' + password).hexdigest():
        return user

    return None


def change_user_info(user, nick, site):
    '''
    Change the information of a login user after comment.
    '''
    nick = nick.strip()
    nick = nick[:30]
    if len(nick) == 0:
        nick = user.nickname()

    site = site.strip()
    if site == 'http://':
        site = None
    if not site:
        site = None

    userinfo = User.all().filter('user = ', user).get()
    if not userinfo:
        userinfo = User(user = user)

    try:
        userinfo.dispname = nick
        userinfo.website = site
        userinfo.put()
    except Exception, e:
        pass

# 2008-06-30 by No.0023
postIdPattern = re.compile('\d+$')
