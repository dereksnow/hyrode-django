from django.db import models
from django.contrib.auth.models import User
import tagging

class Link(models.Model):
	url = models.URLField(unique=True)

	def __unicode__(self):
		return self.url

class Bookmark(models.Model):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)	

	def __unicode__(self):
		return u' %s, %s, %s' % (self.title, self.user.username, 
			self.link.url)

# Register Models with django-tagging
tagging.register(Bookmark)




