from django import forms
from tagging import forms as tag_forms

class BookmarkSaveForm(forms.Form):
	url = forms.URLField(label=u'URL', 
		widget=forms.TextInput(attrs={'size': 64}))
	title = forms.CharField(label=u'Title', 
		widget=forms.TextInput(attrs={'size':64}))
	tags = tag_forms.TagField(label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64}))
