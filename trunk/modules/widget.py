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

from models import Post, Comment, Tag, BlogRoll, AccessLogger
from config import config, global_vars
from google.appengine.ext.webapp import template


def render_s(template, values):
    from django.template import Context, Template
    t = Template(template)
    c = Context(values)
    return t.render(c)

theme = global_vars['theme']


def render_sidebar(values):
    if config.custom_sidebar:
        return render_s(config.custom_sidebar.encode('utf-8'), values)


def recentcomments(values):
    recent_comments = Comment.all().order('-date').fetch(
                      config.recent_comments)
    values.update({
        'recent_comments': recent_comments,
        })
    return template.render(theme.recentcomments_widget, values)


def recentposts(values):
    recent_posts = Post.all().order('-date').fetch(config.recent_posts)
    values.update({
        'recent_posts': recent_posts,
        })
    return template.render(theme.recentposts_widget, values)


def blogroll(values):
    roll = BlogRoll.all().order('text')
    values.update({
        'blogroll': roll,
        })
    return template.render(theme.blogroll_widget, values)


def tags(values):
    tags = Tag.all().order('-count')
    values.update({
        'tags': tags,
        })
    return template.render(theme.tags_widget, values)


def bloglogger(values):
    #accessLogger_cnt = AccessLogger.all().count()
    post_cnt = Post.all().count()
    comment_cnt = Comment.all().count()

    values.update({
        #'accessLogger_cnt': accessLogger_cnt,
        'post_cnt': post_cnt,
        'comment_cnt': comment_cnt,
        })
    return template.render(theme.bloglogger_widget, values)
