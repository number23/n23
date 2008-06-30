from google.appengine.ext import db

__all__ = ['Post', 'Comment', 'Tag', 'Admin', 'User', 'UploadFile', 'BlogRoll']

class Post(db.Model):
	title = db.StringProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)
	author = db.UserProperty(required=True)
	content = db.TextProperty(required=True)
	last_modify_date = db.DateTimeProperty()
	last_modify_by = db.UserProperty()
	tags = db.StringListProperty()

	def comment_count(self):
		comments = Comment.all().filter('post = ', self)
		cnt = comments.count()
		if cnt == 0:
			return 'No Comments'
		if cnt == 1:
			return '1 Comment'

		return '%d Comments' % cnt

	def author_disp(self):
		admin = Admin.all().filter('user = ', self.author).get()
		return unicode(admin)

class Comment(db.Model):
	post = db.ReferenceProperty(Post)
	date = db.DateTimeProperty(auto_now_add=True)
	author = db.UserProperty(required=True)
	content = db.TextProperty(required=True)
	last_modify_date = db.DateTimeProperty()
	last_modify_by = db.UserProperty()

	def author_disp(self):
		user = User.all().filter('user = ', self.author).get()
		if user:
			return unicode(user)
		else:
			return self.author.nickname()

	def author_with_url(self):
		user = User.all().filter('user = ', self.author).get()
		if user:
			if (user.website):
				return u'<a href="%s" target="_blank">%s</a>' % (user.website, user)
			else:
				return unicode(user)
		else:
			return self.author.nickname()


class Tag(db.Model):
	name = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True)


class Admin(db.Model):
	user = db.UserProperty(required = True)
	dispname = db.StringProperty()
	#api_password = db.StringProperty()

	def __unicode__(self):
		if self.dispname:
			return self.dispname
		else:
			return self.user.nickname()

	def __str__(self):
		return self.__unicode__().encode('utf-8')

class User(db.Model):
	user = db.UserProperty(required = True)
	dispname = db.StringProperty()
	website = db.LinkProperty()

	def __unicode__(self):
		if self.dispname:
			return self.dispname
		else:
			return self.user.nickname()

	def __str__(self):
		return self.__unicode__().encode('utf-8')


class UploadFile(db.Model):
	data = db.BlobProperty()
	orig_name = db.StringProperty()
	ext = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

	def name(self):
		if self.ext:
			return str(self.key()) + '.' + self.ext
		else:
			return str(self.key())


class BlogRoll(db.Model):
	url = db.LinkProperty(required=True)
	text = db.StringProperty(required=True)
	description = db.StringProperty()

