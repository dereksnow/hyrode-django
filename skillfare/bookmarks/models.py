from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from djangoratings.fields import RatingField

# TimeStampedModel provides an automatic created and 
# modified field to all models that inherit from it.

class Link(TimeStampedModel):
    url = models.URLField(unique=True)
    rating = RatingField(range=5, can_change_vote=True)

    def __unicode__(self):
        return self.url

class Bookmark(TimeStampedModel):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    # private = models.BooleanField(default=False)
    tags = TaggableManager()
    
    def __unicode__(self):
        return u' %s, %s, %s, %s' % (self.title, self.user.username, 
            self.link.url, self.created)

class Poll(TimeStampedModel):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.ForeignKey(Link)

    def count_choices(self):
        return self.choice_set.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    def __unicode__(self):
        return self.question

class Choice(TimeStampedModel):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    pos = models.SmallIntegerField(default='0')

    def count_votes(self):
        return self.vote_set.count()

    def __unicode__(self):
        return self.choice

    class Meta:
        ordering = ['pos']



class Vote(TimeStampedModel):
    user = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)
    poll = models.ForeignKey(Poll)
    ip = models.IPAddressField()

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)

    class Meta:
        unique_together = (('user', 'poll'))
