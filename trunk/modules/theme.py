import os
import logging

class Theme:
	def __init__(self, name='default'):
		self.name = name
		self.mapping_cache = {}
		self.dir = '/themes/%s' % name
		self.server_dir = os.path.join(os.getcwd(), 'themes', self.name)

	def __getattr__(self, name):
		if self.mapping_cache.has_key(name):
			return self.mapping_cache[name]
		else:
			path = os.path.join(self.server_dir, 'templates', name + '.html')
			if not os.path.exists(path):
				path = os.path.join(os.getcwd(), 'themes', 'default', 'templates', name + '.html')
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

