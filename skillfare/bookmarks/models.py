from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

# TimeStampedModel provides an automatic created and 
# modified field to all models that inherit from it.

class Link(TimeStampedModel):
	url = models.URLField(unique=True)

	def __unicode__(self):
		return self.url

class Bookmark(TimeStampedModel):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)
	tags = TaggableManager()

	def __unicode__(self):
		return u' %s, %s, %s, %s' % (self.title, self.user.username, 
			self.link.url, self.created)





