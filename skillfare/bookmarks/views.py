# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User

def main_page(request):
	template = get_template('main_page.html')
	variables = Context({'head_title': u'SkillFare', 
		'page_title': u'SkillFare', 
		'page_body': u'Find, Share & Organize your Learning Resources'})
	output = template.render(variables)
	return HttpResponse(output)

def user_page(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		raise Http404(u'Requested user not found.')

	bookmarks = user.bookmark_set.all()

	template = get_template('user_page.html')
	variables = Context({'username': username, 'bookmarks': bookmarks})
	output = template.render(variables)
	return HttpResponse(output)

