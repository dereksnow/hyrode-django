# Create your views here.
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from bookmarks.models import Bookmark, Link
from bookmarks.forms import BookmarkSaveForm
from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView
from bookmarks.models import Bookmark


class BookmarkDetailView(DetailView):
	model = Bookmark
	template_name = 'detail.html'

def main_page(request):
	variables = {'user': request.user}
	return render(request, 'main_page.html', variables)

def user_page(request, username):
	user = get_object_or_404(User, username=username)
	bookmarks = user.bookmark_set.order_by('-id')
	variables = {'username': username, 'bookmarks': bookmarks, 
	'show_tags': True}
	return render(request, 'user_page.html', variables)

@login_required
def bookmark_save_page(request):
	if request.method == 'POST':
		form = BookmarkSaveForm(request.POST)
		if form.is_valid():
			# Create or get link.
			link, dummy = Link.objects.get_or_create(
				url=form.cleaned_data['url'])
			# Create or get bookmark.
			bookmark, created = Bookmark.objects.get_or_create(
				user=request.user, 
				link=link
				)
			#Update bookmark title. 
			bookmark.title = form.cleaned_data['title']

			# Save bookmark to database.
			bookmark.save()

			# Using django-taggit tags added after bookmark is saved
			# Get tags from form
			tags = form.cleaned_data['tags']

			for tag in tags:
				bookmark.tags.add(tag)
			
			return HttpResponseRedirect('/user/%s/' % request.user.username)
	else:
		form = BookmarkSaveForm()
	variables = {'form': form}
	return render(request, 'bookmark_save.html', variables)

def tag_page(request, tag_name):
	#tag = get_object_or_404(Tag, name=tag_name)
	bookmarks = Bookmark.objects.filter(tags__name=tag_name).order_by('-modified')
	variables = {'bookmarks': bookmarks, 'tag_name': tag_name,
					'show_tags': True, 'show_user': True}
	return render(request, 'tag_page.html', variables)

				


