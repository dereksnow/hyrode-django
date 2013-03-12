from django.conf.urls import patterns, include, url
from bookmarks.views import *
from django.contrib.auth import views as auth_views
from password_validation.forms import ValidPasswordRegistrationForm, ValidPasswordChangeForm
from registration.views import register
from djangoratings.views import AddRatingFromModel

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	# Browsing
	url(r'^$', main_page),
	url(r'^user/([\w.@+-]+)/$', user_page),
	url(r'^tag/([-\w]+)/$', tag_page),
    url(r'^delete/(?P<pk>\d+)/$', delete_bookmark), 

	url(regex=r'^(?P<pk>\d+)/$', view=BookmarkDetailView.as_view(), 
		name='detail'),

    #Learn Level Voting
    url(r'^level_vote/(?P<pk>\d+)/(?P<level>[-\w]+)/$', level_vote),

    # Ratings
    url(r'^rate/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'bookmarks',
        'model': 'bookmark',
        'field_name': 'rating',
    }),    

	# Search
	url(r'^search/', include('haystack.urls')),

	# Session Management
    url(r'^accounts/register/$', register,
		{'backend': 'registration.backends.default.DefaultBackend', 
	 	'form_class': ValidPasswordRegistrationForm},
		name='registration_register'),

	url(r'^accounts/password/change/$', auth_views.password_change, 
		{'password_change_form': ValidPasswordChangeForm},
		name='auth_password_change'),    

	url(r'^accounts/', include('registration.urls')),

	# Account management
	url(r'^save/link/$', bookmark_save_link),
    url(r'^save/bookmark/$', bookmark_save),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
