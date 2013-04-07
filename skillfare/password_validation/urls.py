from django.conf.urls import patterns, include, url
from forms import ValidPasswordRegistrationForm, ValidPasswordChangeForm
from registration.backends.default.views import RegistrationView
from django.contrib.auth import views as auth_views
    
urlpatterns = patterns('',

    url(r'^register/$', RegistrationView.as_view(form_class=ValidPasswordRegistrationForm),
        name='skillfare_registration_register'),

    url(r'^password/change/$', auth_views.password_change, 
        {'password_change_form': ValidPasswordChangeForm},
        name='skillfare_auth_password_change'),   

)    