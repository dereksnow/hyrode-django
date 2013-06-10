from django import forms
from bookmarks.models import Feature
from taggit.forms import TagField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Field
from crispy_forms.bootstrap import InlineCheckboxes, PrependedText

class BookmarkSaveForm(forms.Form):
	# url = forms.URLField(label=u'URL', 
	# 	widget=forms.TextInput(attrs={'size': 64}))
	title = forms.CharField(
		label=u'Title', 
		widget=forms.TextInput(attrs={'size':64})
	)
	personal = forms.BooleanField(
		label=u'Private Resource',
		required=False
	)
	tags = TagField(
		label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64})
	)
	features = forms.ModelMultipleChoiceField(
		queryset=Feature.objects.all(), 
		required=False, 
		widget=forms.CheckboxSelectMultiple
	)

	def __init__(self, *args, **kwargs):
		super(BookmarkSaveForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'save-form'
		self.helper.form_method = 'post'
		self.helper.form_action = 'bookmarks.views.bookmark_save'
		self.helper.layout = Layout (
			Div(
				Fieldset (
					'Save Resource',
					Div(
						Field('title', css_class='span4', placeholder="title"),
						InlineCheckboxes('features'),
						Field('tags', placeholder="tags"),
						'personal',
						Submit('submit', 'Save'),
						css_class ='well'
					),
				),
				css_class = 'span5'
			)
			

		)
		
	def clean_tags(self):
		tags = self.cleaned_data['tags']
		tags_lower = [tag.lower() for tag in tags]
		return tags_lower

class LinkSaveForm(forms.Form):
	url = forms.URLField(label=u'URL', 
		widget=forms.TextInput(attrs={'size': 64}))

	def __init__(self, *args, **kwargs):
		super(LinkSaveForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'link-form'
		self.helper.form_method = 'post'
		self.helper.form_action = '.'
		self.helper.layout = Layout (
			Div(
				Fieldset (
					'Add Resource Link',
					Div(
						Field('url', css_class='span4', placeholder="http://"),
						Submit('submit', 'Add Link'),
						css_class ='well'
					),
				),
				css_class = 'span5'
			)
			

		)


