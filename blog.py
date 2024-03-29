#! /usr/bin/env python
# -*- coding: utf-8 -*-

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


import sys
import os
import datetime
import urllib2
import wsgiref.handlers
import re

sys.path.append('modules')
from modules.base import *
from modules.models import *
from modules import PyRSS2Gen
from modules.theme import Theme, ThemeIterator
from modules.config import Config

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from mimetypes import types_map


class NewPost(BaseRequestHandler):

    def get(self):
        if self.chk_admin():
            self.current_page = "new"
            self.template_values.update({
                'mode': 'new',
                })
            self.render(self.theme.editpost_page)

    def post(self):
        if self.chk_admin():
            title = self.param('title')
            content = self.param('post_content')
            tags = split_tags(self.param('tags'))

            try:
                postid = new_post(title = title, author = self.login_user,
                                  content = content, tags = tags)

                self.redirect('/blog/post/%d' % postid)
            except db.BadValueError, e:
                self.redirect('/blog/')


class NewComment(BaseRequestHandler):

    def post(self):
        if self.chk_login():
            content = self.param('comment_content')
            postid = self.param('postid')
            nick = self.param('nick')
            site = self.param('site')
            post = Post.get_by_id(int(postid))

            try:
                comment = Comment(post = post,
                                  content = content,
                                  author = self.login_user)
                comment.put()
                change_user_info(self.login_user, nick, site)
                self.redirect('/blog/post/%s' % postid)
            except db.BadValueError, e:
                self.redirect('/blog/')


class EditPost(BaseRequestHandler):

    def get(self):
        if self.chk_admin():
            self.current_page = "new"
            #postid = self.request.path[15:]
            postid = postIdPattern.findall(self.request.path)[0]
            post = Post.get_by_id(int(postid))
            self.template_values.update({
                'post': post,
                'mode': 'edit',
                })
            self.render(self.theme.editpost_page)

    def post(self):
        if self.chk_admin():
            #postid = self.request.path[15:]
            postid = postIdPattern.findall(self.request.path)[0]
            edit_post(postid = postid,
                      title = self.param('title'),
                      content = self.param('post_content'),
                      tags = split_tags(self.param('tags')))

            self.redirect('/blog/post/%s' % postid)


class EditComment(BaseRequestHandler):

    def get(self):
        # TODO
        self.redirect('/blog/')

    def post(self):
        # TODO
        self.redirect('/blog/')


class DeletePost(BaseRequestHandler):

    def get(self):
        if self.chk_admin():
            postid = self.param('postid')
            delete_post(postid)
            self.redirect('/blog/')


class DeleteComment(BaseRequestHandler):

    def get(self):
        if self.chk_login():
            commentid = self.param('commentid')
            comment = Comment.get_by_id(int(commentid))
            if self.login_user == comment.author or self.is_admin:
                postid = comment.post.key().id()
                comment.delete()
                self.redirect('/blog/post/%d' % postid)
            else:
                self.redirect('/blog/')


class PostList(BaseRequestHandler):

    def get(self):
        self.current_page = "home"
        tag_pattern = re.compile('^/blog/tag/(.*)')
        tag_list = tag_pattern.findall(self.request.path)
        tag = ''
        if tag_list:
            tag = tag_list[0]
            if tag.find('/') != -1:
                tag = tag[:tag.find('/')]
            tag = urllib2.unquote(urllib2.unquote(tag)).decode('utf-8')
            all_posts = Post.all().filter('tags =', tag)
        else:
            all_posts = Post.all()

        page_size = config.posts_per_page
        max_page = (all_posts.count() + page_size - 1) / page_size
        page = 1
        page_pattern = re.compile('/page/(\d+)$')
        pattern_list = page_pattern.findall(self.request.path)
        if pattern_list:
            page = int(pattern_list[0])
        if page > max_page:
            page = max_page
        if page <= 0:
            page = 1
        offset = (page - 1) * page_size
        posts = all_posts.order('-date').fetch(page_size, offset = offset)

        show_prev = False
        show_next = False
        show_prev = not (page == 1)
        show_next = not (page == max_page)
        page_list = []
        cnt = 1
        while cnt < max_page:
            page_list.append(cnt)
            cnt += 1

        self.template_values.update({
                'tag': tag,
                'posts': posts,
                'post_count': all_posts.count(),
                'show_prev': show_prev,
                'show_next': show_next,
                'prev': page - 1,
                'next': page + 1,
                'page': page,
                'max_page': max_page,
                'page_list': page_list,
                })
        self.render(self.theme.postlist_page)


class ViewPost(BaseRequestHandler):

    def get(self):
        self.current_page = "home"
        #postid = self.request.path[11:]
        postid = postIdPattern.findall(self.request.path)[0]
        post = Post.get_by_id(int(postid))
        comments = Comment.all().filter('post = ', post).order('date')

        if not post:
            self.redirect('/static/pages/404.html')
        else:
            self.template_values.update({
                    'post': post,
                    'comments': comments,
                    })

            self.render(self.theme.viewpost_page)


class Customize(BaseRequestHandler):

    def get(self):
        if self.chk_admin():
            self.current_page = "config"
            # put the class definition here to avoid caching,
            # because we need it list theme dir every time

            class ConfigForm(djangoforms.ModelForm):

                theme = djangoforms.forms.CharField(
                widget = djangoforms.forms.Select(choices = ThemeIterator()))

                class Meta:
                    model = config
                    exclude = ('last_config_time')
            config_form = ConfigForm(instance = config)
            self.template_values.update({
                'config_form': config_form,
                })

            self.render(self.theme.config_page)

    def post(self):
        if self.chk_admin():
            # put the class definition here to avoid caching,
            # because we need it list theme dir every time

            class ConfigForm(djangoforms.ModelForm):
                theme = djangoforms.forms.CharField(
                widget = djangoforms.forms.Select(choices = ThemeIterator()))

                class Meta:
                    model = Config
                    exclude = ('last_config_time')
            config_form = ConfigForm(data = self.request.POST,
                                     instance = config)
            if config_form.is_valid():
                config_form.save(commit=False)
                config.last_config_time = \
                    datetime.datetime.utcnow().replace(microsecond=0)
                config.put()

                global_vars['theme'] = Theme(config.theme)

                self.redirect('/blog/')
            else:
                self.template_values.update({
                    'config_form': config_form,
                    })

                self.render(self.theme.config_page)


class RssFead(BaseRequestHandler):

    def get(self):
        blog_items = []
        feed_title = config.blog_title
        if self.request.path.startswith('/blog/feed/tag/'):
            # here too, i need unquote twice -_-
            tag = urllib2.unquote(urllib2.unquote(
                self.request.path[15:])).decode('utf-8')
            feed_title += 'Tag: ' + tag
            posts = Post.all().filter('tags = ',
                    tag).order('-date').fetch(config.rss_posts)
        elif self.request.path.startswith('/blog/feed'):
            posts = Post.all().order('-date').fetch(config.rss_posts)

        for post in posts:
            post_url = '%s/blog/post/%d' % (self.request.host_url,
                                            post.key().id())
            blog_items.append(PyRSS2Gen.RSSItem(
                title = post.title,
                author = post.author.nickname(),
                link = post_url,
                description = post.content,
                pubDate = post.date,
                guid = PyRSS2Gen.Guid(post_url),
                categories = post.tags))

        rss = PyRSS2Gen.RSS2(
            title = config.blog_title,
            link = self.request.host_url + '/blog/',
            description = 'latest %d posts of %s' % (min(len(blog_items),
                                                     config.rss_posts),
                                                     config.blog_title),
            lastBuildDate = datetime.datetime.utcnow(),
            items = blog_items)

        self.response.headers['Content-Type'] = \
            'application/rss+xml; charset=utf-8'
        self.write(rss.to_xml(encoding='utf-8'))


class LogInOut(BaseRequestHandler):

    def get(self):
        if self.request.path == '/blog/login':
            self.redirect(self.get_login_url(True))

        if self.request.path == '/blog/logout':
            self.redirect(self.get_logout_url(True))


class Upload(BaseRequestHandler):

    def get(self):
        filename = self.request.path[13:]
        split = filename.rfind('.')
        if split == -1:
            name, ext = filename, ''
        else:
            name = filename[:split]
            ext = filename[split + 1:]

        file = UploadFile.get(db.Key(name))
        if not file:
            self.redirect('/static/pages/404.html')
        elif file.ext != ext:
            self.redirect('/static/pages/404.html')
        else:
            ext = '.' + ext
            mimetype = 'application/octet-stream'
            if ext in types_map:
                mimetype = types_map[ext]
            self.response.headers['Content-Type'] = mimetype
            self.response.headers['Content-Disposition'] = \
                'inline; filename="' + file.orig_name.encode('utf-8') + '"'
            self.write(file.data)

    def post(self):
        if self.chk_admin():
            filename = self.param('filename')
            fileext = self.param('fileext')
            data = self.param('upfile')
            UploadFile(orig_name = filename, ext = fileext, data = data).put()
            self.redirect('/blog/filemanager')


class FileManager(BaseRequestHandler):

    def get(self):
        if self.chk_admin():
            self.current_page = "upload"
            files = UploadFile.all().order('-date')
            self.template_values.update({
                'files': files,
                })
            self.render(self.theme.filemanager_page)

    def post(self): # delete files
        if self.chk_admin():
            delids = self.request.POST.getall('del')
            if delids:
                for id in delids:
                    file = UploadFile.get_by_id(int(id))
                    file.delete()

            self.redirect('/blog/filemanager')


class BlogRollManager(BaseRequestHandler):

    def get(self): # delete a link
        if self.chk_admin():
            delid = self.param('delid')
            bloglink = BlogRoll.get_by_id(int(delid))
            if bloglink:
                bloglink.delete()

            self.redirect(self.referer)

    def post(self): # add a link
        if self.chk_admin():
            try:
                bloglink = BlogRoll(url = self.param('url'),
                                    text = self.param('text'),
                                    description = self.param('description'))
                bloglink.put()
            except:
                pass

            self.redirect(self.referer)


class NotFound(BaseRequestHandler):

    def get(self):
        self.redirect('/static/pages/404.html')


def main():
    webapp.template.register_template_library('filter')
    application = webapp.WSGIApplication(
            [
                #('/', PostList),
                ('/blog', PostList),
                ('/blog/', PostList),
                ('/blog/page/\\d+', PostList),
                ('/blog/tag/.+/page/\\d+', PostList),
                ('/blog/tag/.+', PostList),
                ('/blog/post/\\d+', ViewPost),
                ('/blog/newpost', NewPost),
                ('/blog/newcomment', NewComment),
                ('/blog/editpost/\\d+', EditPost),
                ('/blog/editcomment/\\d+', EditComment),
                ('/blog/deletepost', DeletePost),
                ('/blog/deletecomment', DeleteComment),
                ('/blog/custom', Customize),
                ('/blog/feed', RssFead),
                ('/blog/feed/tag/.+', RssFead),
                ('/blog/login', LogInOut),
                ('/blog/logout', LogInOut),
                ('/blog/upload', Upload),
                ('/blog/upload/.+', Upload),
                ('/blog/upload/', FileManager),
                ('/blog/filemanager', FileManager),
                ('/blog/addbloglink', BlogRollManager),
                ('/blog/delbloglink', BlogRollManager),
                #('.*', NotFound),
                ],
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
