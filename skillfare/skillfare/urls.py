from django.conf.urls import patterns, include, url
from bookmarks.views import *
from django.contrib.auth import views as auth_views
from password_validation.forms import ValidPasswordRegistrationForm, ValidPasswordChangeForm
from registration.views import register

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	# Browsing
	url(r'^$', main_page),
	url(r'^user/([\w.@+-]+)/$', user_page),

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
	url(r'^save/$', bookmark_save_page),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
