from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from djangoratings.fields import RatingField
from django.utils.text import slugify

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
    private = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, blank=True, default='')
    tags = TaggableManager()
    
    def __unicode__(self):
        return u' %s, %s, %s, %s' % (self.title, self.user.username, 
            self.link.url, self.created)

    def save(self, *args, **kwargs):
        # check if newly created
        if not self.slug:
            # newly created, so set slug value
            self.slug = slugify(self.title)
        super(Bookmark, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id), self.slug])

class Poll(TimeStampedModel):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.ForeignKey(Link)

    def __unicode__(self):
        return self.question

    def count_choices(self):
        return self.choice_set.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

class Choice(TimeStampedModel):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    pos = models.SmallIntegerField(default='0')

    class Meta:
        ordering = ['pos']

    def __unicode__(self):
        return self.choice

    def count_votes(self):
        return self.vote_set.count()

class Vote(TimeStampedModel):
    user = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)
    poll = models.ForeignKey(Poll)
    ip = models.IPAddressField()

    class Meta:
        unique_together = (('user', 'poll'))

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)

