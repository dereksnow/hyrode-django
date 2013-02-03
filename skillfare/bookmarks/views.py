# Create your views here.
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User

def main_page(request):
	variables = {'user': request.user}
	return render(request, 'main_page.html', variables)

def user_page(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404(u'Requested user not found.')

	bookmarks = user.bookmark_set.all()

	variables = {'username': username, 'bookmarks': bookmarks}
	return render(request, 'user_page.html', variables)

