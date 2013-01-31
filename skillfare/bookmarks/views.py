# Create your views here.
from django.http import HttpResponse

def main_page(request):
	output = u'''
		<html>
			<head><title>%s</title></head>
			<body>
				<h1>%s</h1><p>%s</p>
			</body>
		</html>
			''' % (u'Skillfare', 
				u'Skillfare',
			 u'Find, Share & Organize your Learning Resources')
	return HttpResponse(output)

