from django import forms
from taggit.forms import TagField

class BookmarkSaveForm(forms.Form):
	# url = forms.URLField(label=u'URL', 
	# 	widget=forms.TextInput(attrs={'size': 64}))
	title = forms.CharField(label=u'Title', 
		widget=forms.TextInput(attrs={'size':64}))
	# private = forms.BooleanField(label=u'Keep Private',
	# 	required=False)
	tags = TagField(label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64}))


	def clean_tags(self):
		tags = self.cleaned_data['tags']
		tags_lower = [tag.lower() for tag in tags]
		return tags_lower

class LinkSaveForm(forms.Form):
	url = forms.URLField(label=u'URL', 
		widget=forms.TextInput(attrs={'size': 64}))


