from django.conf.urls import patterns, include, url
from bookmarks.views import *
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
	url(r'^bookmarks/tag/([-\w]+)/$', tag_page),
    url(r'^delete/(?P<pk>\d+)/$', view=delete_bookmark, name='bookmark_delete'), 

    url(r'bookmark/interested/(?P<pk>\d+)/$', interest_vote),
    url(r'bookmark/report_abuse/(?P<pk>\d+)/$', report_abuse_vote),

	url(regex=r'^bookmark/detail/(?P<pk>\d+)/(?P<slug>[-\w]*)/?$', view=bookmark_detail, 
		name='bookmark_detail'),

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

	url(r'^accounts/', include('registration.backends.default.urls')),

	# Account management
	url(r'^link/save/$', bookmark_save_link),
    url(r'^bookmark/save/$', bookmark_save),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
