# Create your views here.
from django.http import Http404
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def main_page(request):
	variables = Context({'user': request.user})
	return render_to_response('main_page.html', variables)

def user_page(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404(u'Requested user not found.')

	bookmarks = user.bookmark_set.all()

	variables = Context({'username': username, 'bookmarks': bookmarks})
	return render_to_response('user_page.html', variables)

