from django import template
register = template.Library()

@register.filter(name='font_icon')
def get_font_icon(key):
    bookmark_features = {'Certificates':'icon-trophy', 'Feedback':'icon-exchange', 'Sandbox':'icon-beaker', 'Video':'icon-film'}
    return bookmark_features.get(key)