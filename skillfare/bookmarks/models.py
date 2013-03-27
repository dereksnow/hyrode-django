from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager
from djangoratings.fields import RatingField
from django.utils.text import slugify
from datetime import datetime

try:
    from django.utils.timezone import now as now
except ImportError:
    now = datetime.now

# TimeStampedModel provides an automatic created and 
# modified field to all models that inherit from it.


class PollBase(TimeStampedModel):
    question = models.CharField(max_length=255)
    #description = models.TextField(blank=True)

    class Meta:
        abstract = True    

    def __unicode__(self):
        return self.question

class SingleChoicePoll(PollBase):

    def count_votes(self):
        return self.singlechoicevote_set.count()


class MultiChoicePoll(PollBase):
    #question = models.CharField(max_length=255)
    #description = models.TextField(blank=True)

    def count_choices(self):
        return self.choice_set.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result


class Link(TimeStampedModel):
    url = models.URLField(unique=True)
    rating = RatingField(range=5, can_change_vote=True)
    learn_level_poll = models.OneToOneField(MultiChoicePoll)

    def __unicode__(self):
        return self.url

class Feature(TimeStampedModel):
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % (self.description)

    class Meta:
        ordering = ['description']        

class Bookmark(TimeStampedModel):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    private = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, blank=True, default='')
    features = models.ManyToManyField(Feature)
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


class SharedBookmark(TimeStampedModel):
    bookmark = models.OneToOneField(Bookmark)
    interest_poll = models.OneToOneField(SingleChoicePoll, related_name='shared_bookmark')
    report_abuse_poll = models.OneToOneField(SingleChoicePoll)
    # slug = models.SlugField(max_length=255, blank=True, default='')
    hot_score = models.PositiveIntegerField()
    
    def __unicode__(self):
        return u' %s, %s' % (self.bookmark, self.hot_score)

    # def save(self, *args, **kwargs):
    #     # check if newly created
    #     if not self.slug:
    #         # newly created, so set slug value
    #         self.slug = self.bookmark.slug
    #     super(SharedBookmark, self).save(*args, **kwargs)

    def get_hot_score(self):
        # Based on Hacker News Ranking Algorithm
        td = now() - self.created 
        age_hours = td.days * 24 + (float(td.seconds) / 3600)  
        return (self.interest_poll.count_votes()) / pow(age_hours + 2, 0.5)



class Choice(TimeStampedModel):
    poll = models.ForeignKey(MultiChoicePoll)
    choice = models.CharField(max_length=255)
    pos = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['pos']

    def __unicode__(self):
        return self.choice

    def count_votes(self):
        return self.multichoicevote_set.count()

class VoteBase(TimeStampedModel):
    user = models.ForeignKey(User)    
    ip = models.IPAddressField()

    class Meta:
        abstract = True
        unique_together = (('user', 'poll'))

class MultiChoiceVote(VoteBase):
    poll = models.ForeignKey(MultiChoicePoll)
    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)

class SingleChoiceVote(VoteBase):
    poll = models.ForeignKey(SingleChoicePoll)

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)        




