from django.conf.urls import patterns, include, url
from bookmarks.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', main_page),
	url(r'^user/(\w+)/$', user_page),
	url(r'^accounts/', include('registration.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
