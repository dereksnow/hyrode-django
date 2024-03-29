from django.conf.urls import patterns, include, url
from bookmarks.views import *
from bookmarks.models import Bookmark
#from django.contrib.auth import views as auth_views
#from password_validation.forms import ValidPasswordRegistrationForm, ValidPasswordChangeForm
#from registration.views import register
from djangoratings.views import AddRatingFromModel

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	# Browsing
	url(r'^$', main_page),
	url(r'^user/([\w.@+-]+)/$', user_page),
    url(r'^user/([\w.@+-]+)/create_path/$', view=create_path, name='create_path'),
    # url(r'^user/([\w.@+-]+)/path_save/$', view=path_save, name='path_save'),
    url(r'^path/save/$', view=path_save, name='path_save'),
	url(r'^bookmarks/tag/([-\w]+)/$', view=tag_page),
    url(r'^delete/(?P<pk>\d+)/$', view=delete_bookmark, name='bookmark_delete'), 

    url(r'^search/$', view=search),

    url(r'^bookmark/interested/(?P<pk>\d+)/$', interest_vote, {'model': SharedBookmark}, name="interest_vote_bookmark"),
    url(r'^path/interested/(?P<pk>\d+)/$', interest_vote, {'model': SharedPath}, name="interest_vote_path"),

    url(r'bookmark/report_abuse/(?P<pk>\d+)/$', report_abuse_vote, {'model': SharedBookmark}, name="abuse_vote_bookmark"),
    url(r'path/report_abuse/(?P<pk>\d+)/$', report_abuse_vote, {'model': SharedPath}, name="abuse_vote_path"),

	url(regex=r'^bookmark/detail/(?P<pk>\d+)/(?P<slug>[-\w]*)/?$', view=bookmark_detail, 
		name='bookmark_detail'),

    url(regex=r'^path/detail/(?P<pk>\d+)/(?P<slug>[-\w]*)/?$', view=path_detail, 
        name='path_detail'),    

    url(regex=r'^sharedbookmark/detail/(?P<pk>\d+)/(?P<slug>[-\w]*)/?$', view=shared_bookmark_detail, 
        name='sharedbookmark_detail'),    

    #Learn Level Voting
    url(r'^bookmark/level_vote/(?P<pk>\d+)/(?P<level>[-\w]+)/$', level_vote),

    # Ratings
    url(r'^bookmark/rate/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'bookmarks',
        'model': 'link',
        'field_name': 'rating',
    }, name='bookmark_rate'),    

    url(r'^path/rate/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'bookmarks',
        'model': 'path',
        'field_name': 'rating',
    }, name='path_rate'),        

	# Search
	url(r'^bookmarks/search/', include('haystack.urls')),

	# Session Management

    # The following url functions are being used to provide
    # custom validation forms. When you provide html to 
    # url reversal ensure that the 'name's below are being used
    # These names will distinquish from the url functions 
    # used in the registration app which has a weaker password
    # validation.
 #    url(r'^accounts/register/$', register,
	# 	{'backend': 'registration.backends.default.DefaultBackend', 
	#  	'form_class': ValidPasswordRegistrationForm},
	# 	name='skillfare_registration_register'),

	# url(r'^accounts/password/change/$', auth_views.password_change, 
	# 	{'password_change_form': ValidPasswordChangeForm},
	# 	name='skillfare_auth_password_change'),    

    url(r'^accounts/', include('password_validation.urls')),

    # override logout mapping provided in django-registration
    # logout will redirect to landing page
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),

	url(r'^accounts/', include('registration.backends.default.urls')),

	# Account management
	url(r'^link/save/$', bookmark_save_link),
    url(r'^bookmark/save/$', bookmark_save),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
