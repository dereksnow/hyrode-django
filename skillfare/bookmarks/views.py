import urllib
from bs4 import BeautifulSoup

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from bookmarks.models import Bookmark, Link, Poll, Choice, Vote
from bookmarks.forms import BookmarkSaveForm, LinkSaveForm
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.views.generic import DetailView
from bookmarks.models import Bookmark


class BookmarkDetailView(DetailView):
    model = Bookmark
    template_name = 'detail.html'

def main_page(request):
    variables = {'user': request.user}
    return render(request, 'main_page.html', variables)

def user_page(request, username):
    if request.method == 'POST' and request.user.username == username:
        # Is Validation needed?? Investigate
        deletelist = request.POST.getlist('deletelist')
        deletelist = [int(i) for i in deletelist if i.isdigit()] 
        Bookmark.objects.filter(user=request.user,id__in=deletelist).delete()
        return HttpResponseRedirect('/user/%s/' % request.user.username)    
    else:
        show_edit = request.REQUEST.get('show_edit', False) and request.user.username == username
        user = get_object_or_404(User, username=username)
        bookmarks = user.bookmark_set.order_by('-id')
        variables = {
            'username': username, 
            'bookmarks': bookmarks, 
            'show_tags': True,
            'show_edit': show_edit
        }
        return render(request, 'user_page.html', variables)


def delete_bookmark(request, pk):
    redirect_to = request.REQUEST.get('next', '')
    bookmark = get_object_or_404(Bookmark, pk=pk)
    bookmark.delete()
    return HttpResponseRedirect(redirect_to)

@login_required
def level_vote(request, pk, level):
    redirect_to = request.REQUEST.get('next', '')
    
    bookmark = get_object_or_404(Bookmark, pk=pk)
    poll, created = Poll.objects.get_or_create(
        question="Learning Level Poll", 
        bookmark=bookmark
    )

    choice, created = Choice.objects.get_or_create(
        poll=poll, 
        choice=level
    )  

    ip = get_ip(request)

    if Vote.objects.filter(ip=ip).count() < 5:
        try:        
            Vote.objects.get(user = request.user, poll = poll)
        except Vote.DoesNotExist:
            Vote.objects.create(user = request.user, choice=choice, poll=poll, ip=ip)


    return HttpResponseRedirect(redirect_to)

# helper function - should move to another file and import
def get_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


@login_required
def bookmark_save_link(request):
    if request.method == 'POST':
        form = LinkSaveForm(request.POST)
        if form.is_valid():
            # Create or get link.
            link, dummy = Link.objects.get_or_create(
                url = form.cleaned_data['url']
            )

            request.session['link'] = link

            return HttpResponseRedirect('/save/bookmark/')        
    else:
        form = LinkSaveForm()
    variables = {'form': form}
    return render(request, 'bookmark_save_link.html', variables)


@login_required
def bookmark_save(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            # Create or get link.
            # link, dummy = Link.objects.get_or_create(
            #     url=form.cleaned_data['url']
            # )
            # Create or get bookmark.
            # bookmark, created = Bookmark.objects.get_or_create(
            #     user=request.user, 
            #     link=link
            # )

            # Create or get bookmark.
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user, 
                link=request.session.get('link', None)
            )

            #Update bookmark title. 
            bookmark.title = form.cleaned_data['title']

            # Save bookmark to database.
            bookmark.save()

            # Create poll for learning level.
            poll = Poll.objects.create(
                question = "Learning Level Poll",
                bookmark = bookmark
            )

            # Create choices for learning level poll.
            beginner_choice = Choice.objects.create(poll=poll, choice='beginner', pos=0)
            intermediate_choice = Choice.objects.create(poll=poll, choice='intermediate', pos=1)
            advanced_choice = Choice.objects.create(poll=poll, choice='advanced', pos=2)         

            # Using django-taggit tags added after bookmark is saved
            # Get tags from form
            tags = form.cleaned_data['tags']

            for tag in tags:
                bookmark.tags.add(tag)
            
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
        link = request.session.get('link', None)
        if link:
            soup = BeautifulSoup(urllib.urlopen(link.url), "lxml")
            data = {'title': soup.title.string}
        else:
            data = {}
        form = BookmarkSaveForm(initial=data)
    variables = {'form': form}
    return render(request, 'bookmark_save.html', variables)

# def tag_page(request, tag_name):
#   #tag = get_object_or_404(Tag, name=tag_name)
#   bookmarks = Bookmark.objects.filter(tags__name=tag_name).order_by('-modified')
#   variables = {'bookmarks': bookmarks, 'tag_name': tag_name,
#                   'show_tags': True, 'show_user': True}
#   return render(request, 'tag_page.html', variables)

                
def tag_page(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    bookmarks = Bookmark.objects.filter(tags__name=tag.name).order_by('-modified')
    variables = {'bookmarks': bookmarks, 'tag_name': tag.name,
                    'show_tags': True, 'show_user': True}
    return render(request, 'tag_page.html', variables)




