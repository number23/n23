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


class Theme:

    def __init__(self, name='default'):
        self.name = name
        self.mapping_cache = {}
        self.dir = '/themes/%s' % name
        self.server_dir = os.path.join(os.getcwd(), 'themes', self.name)

    def __getattr__(self, name):
        if name in self.mapping_cache:
            return self.mapping_cache[name]
        else:
            path = os.path.join(self.server_dir, 'templates', name + '.html')
            if not os.path.exists(path):
                path = os.path.join(os.getcwd(),
                                    'themes',
                                    'default',
                                    'templates',
                                    name + '.html')
            self.mapping_cache[name] = path
            return path


class ThemeIterator:

    def __init__(self, theme_path='themes'):
        self.iterating = False
        self.theme_path = theme_path
        self.list = []

    def __iter__(self):
        return self

    def next(self):
        if not self.iterating:
            self.iterating = True
            self.list = os.listdir(self.theme_path)
            self.cursor = 0

        if self.cursor >= len(self.list):
            self.iterating = False
            raise StopIteration
        else:
            value = self.list[self.cursor]
            self.cursor += 1
            return (str(value), unicode(value))
