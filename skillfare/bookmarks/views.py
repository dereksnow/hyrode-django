# Create your views here.
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from bookmarks.models import Bookmark, Link
from tagging.models import Tag
from bookmarks.forms import BookmarkSaveForm
from django.contrib.auth.decorators import login_required

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

			#If the bookmark is being updated, clear old tag list.
			#if not created:
			#	bookmark.tag_set.clear()
			# Create new tag list.

			# get tags
			tag_names = form.cleaned_data['tags']
			# update bookmark with tags
			Tag.objects.update_tags(bookmark, tag_names)

			#for tag_name in tag_names:
			#	tag, dummy = Tag.objects.get_or_create(name=tag_name)
			#	bookmark.tag_set.add(tag)

			# Save bookmark to database.
			bookmark.save()
			return HttpResponseRedirect('/user/%s/' % request.user.username)
	else:
		form = BookmarkSaveForm()
	variables = {'form': form}
	return render(request, 'bookmark_save.html', variables)

				


