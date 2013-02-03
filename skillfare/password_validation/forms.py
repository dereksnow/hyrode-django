from django import forms
from registration.forms import RegistrationForm
from django.contrib import auth


class ValidPasswordRegistrationForm(RegistrationForm):

    def clean_password1(self):
        return check_password_length_and_contents(self.cleaned_data.get('password1'))


class ValidPasswordChangeForm(auth.forms.PasswordChangeForm):
    
    def clean_new_password1(self):
        return check_password_length_and_contents(self.cleaned_data.get('new_password1'))



def check_password_length_and_contents(password):

        MIN_LENGTH = 8

        # At least MIN_LENGTH long
        if len(password) < MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % MIN_LENGTH)
        if not any(c.isdigit() for c in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(c.isalpha() for c in password):
            raise forms.ValidationError("Password must contain at least one alphabetic character.")

        return password