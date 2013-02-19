import datetime
from haystack import site
from haystack import indexes
from bookmarks.models import Bookmark


class BookmarkIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')

	# Needed to access tags from django-taggit
	tags = indexes.MultiValueField()

	def prepare_tags(self, obj):
		return [tag.name for tag in obj.tags.all()]		

	def index_queryset(self):
		# Used when entire index for model is updated.
		return Bookmark.objects.filter(modified__lte=datetime.datetime.now())

site.register(Bookmark, BookmarkIndex)