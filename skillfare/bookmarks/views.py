import urllib
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from bookmarks.models import Bookmark, Link, MultiChoicePoll, SingleChoicePoll, Choice, SingleChoiceVote, MultiChoiceVote
from bookmarks.forms import BookmarkSaveForm, LinkSaveForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from taggit.models import Tag
from django.views.generic import DetailView
from bookmarks.models import Bookmark, SharedBookmark
from bookmarks.utils import get_ip


def bookmark_detail(request, pk, slug = ''):
    bookmark = get_object_or_404(Bookmark, pk = pk)
    if bookmark.slug != slug:
        return HttpResponseRedirect(reverse(bookmark_detail, args=[pk, bookmark.slug]))
    variables = {'bookmark': bookmark}
    return render(request, 'detail.html', variables)

def shared_bookmark_detail(request, pk, slug = ''):
    shared_bookmark = get_object_or_404(SharedBookmark, pk = pk)
    if shared_bookmark.slug != slug:
        return HttpResponseRedirect(
            reverse(shared_bookmark_detail, args=[pk, shared_bookmark.slug])
        )
    variables = {'shared_bookmark': shared_bookmark}
    return render(request, 'shared_detail.html', variables)

def main_page(request):
    shared_bookmarks = Bookmark.objects.filter(private=False).order_by('-sharedbookmark__hot_score')[:20]
    variables = {
        'bookmarks': shared_bookmarks,
        'show_tags': True,
        'show_user': True
    }
    return render(request, 'main_page.html', variables)

@login_required
def user_page(request, username):
    if request.method == 'POST' and request.user.username == username:
        # Is Validation needed?? Investigate
        operation = request.POST.get('operation', None)
        if operation:
            # editlist contain bookmark ids
            editlist = request.POST.getlist('editlist')
            editlist = [int(i) for i in editlist if i.isdigit()] 
            bookmark_list = Bookmark.objects.filter(user=request.user,id__in=editlist)
            
            if operation == 'delete':                
                for bookmark in bookmark_list:
                    if bookmark.private == True or (bookmark.private == False and 
                        bookmark.sharedbookmark.interest_poll.count_votes() < 2):
                        bookmark.delete()

            elif operation == 'private':
                for bookmark in bookmark_list:
                    if bookmark.sharedbookmark.interest_poll.count_votes() < 2:
                        bookmark.sharedbookmark.delete()
                        bookmark.private = True

            elif operation == 'public':                
                for bookmark in bookmark_list:
                    _save_sharedbookmark(reqest, bookmark)
                bookmark_list.update(private=False)                    

            #return HttpResponseRedirect('/user/%s/' % request.user.username)    
        return HttpResponseRedirect(reverse(user_page, args=[request.user.username]))    
    else:
        show_edit = request.REQUEST.get('show_edit', False) and request.user.username == username
        user = get_object_or_404(User, username=username)
        shared_bookmarks = SharedBookmark.objects.filter(bookmark__user=user).order_by('-hot_score')
        if user == request.user:
            bookmarks = Bookmark.objects.filter(user=user)
        else:
            bookmarks = None

        #bookmarks = user.bookmark_set.order_by('-id')
        variables = {
            'username': username, 
            'shared_bookmarks': shared_bookmarks,
            'bookmarks': bookmarks, 
            'show_tags': True,
            'show_edit': show_edit,
            'show_single_edit': True
        }
        return render(request, 'user_page.html', variables)


def delete_bookmark(request, pk):
    redirect_to = request.REQUEST.get('next', '')
    bookmark = get_object_or_404(Bookmark, pk=pk)
    bookmark.delete()
    return HttpResponseRedirect(redirect_to)


@login_required
def interest_vote(request, pk):
    redirect_to = request.REQUEST.get('next', '')

    shared_bookmark = get_object_or_404(SharedBookmark, pk=pk)

    ip = get_ip(request)

    if SingleChoiceVote.objects.filter(poll = shared_bookmark.interest_poll, ip = ip).count() <= 5:
        
        try:
            SingleChoiceVote.objects.get(user = request.user, poll = shared_bookmark.interest_poll)
        
        except SingleChoiceVote.DoesNotExist:
            SingleChoiceVote.objects.create(user = request.user, poll = shared_bookmark.interest_poll, ip = ip)

    return HttpResponseRedirect(redirect_to)


@login_required
def report_abuse_vote(request, pk):
    redirect_to = request.REQUEST.get('next', '')

    shared_bookmark = get_object_or_404(SharedBookmark, pk=pk)

    ip = get_ip(request)

    if SingleChoiceVote.objects.filter(poll = shared_bookmark.report_abuse_poll, ip = ip).count() <= 5:
        
        try:
            SingleChoiceVote.objects.get(user = request.user, poll = shared_bookmark.report_abuse_poll)
        except SingleChoiceVote.DoesNotExist:
            if shared_bookmark.report_abuse_poll.count_votes() < 5:
                SingleChoiceVote.objects.create(user = request.user, poll = shared_bookmark.report_abuse_poll, ip = ip)
            else :
                shared_bookmark.bookmark.delete()
                shared_bookmark.delete()
                
            
    return HttpResponseRedirect(redirect_to)




@login_required
def level_vote(request, pk, level):
    redirect_to = request.REQUEST.get('next', '')
    
    link = get_object_or_404(Link, pk=pk)

    choice, created = Choice.objects.get_or_create(
        poll = link.learn_level_poll, 
        choice = level
    )  

    ip = get_ip(request)

    if MultiChoiceVote.objects.filter(poll = link.learn_level_poll, ip=ip).count() <= 5:
        
        try:        
            MultiChoiceVote.objects.get(user = request.user, poll = link.learn_level_poll)
        except MultiChoiceVote.DoesNotExist:
            MultiChoiceVote.objects.create(user = request.user, choice=choice, poll = link.learn_level_poll, ip=ip)


    return HttpResponseRedirect(redirect_to)

@login_required
def bookmark_save_link(request):
    if request.method == 'POST':
        form = LinkSaveForm(request.POST)
        if form.is_valid():

            # get or create link.
            # Did not use get_or_create since a poll is needed to
            # create Link object. 
            try:
                link = Link.objects.get(url = form.cleaned_data['url'])
            except Link.DoesNotExist:

                poll = MultiChoicePoll.objects.create(
                    question = "Learning Level Poll"
                )

                # Create choices for learning level poll.
                Choice.objects.create(poll = poll, choice = 'beginner', pos=0)
                Choice.objects.create(poll = poll, choice = 'intermediate', pos=1)
                Choice.objects.create(poll = poll, choice = 'advanced', pos=2)

                link = Link.objects.create(
                    url = form.cleaned_data['url'], 
                    learn_level_poll = poll
                )
          

            request.session['link'] = link

            return HttpResponseRedirect(reverse(bookmark_save))        
    else:
        form = LinkSaveForm()
    variables = {'form': form}
    return render(request, 'bookmark_save_link.html', variables)


@login_required
def bookmark_save(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark, bookmark_created = _bookmark_save(request, form)

            if not form.cleaned_data['private']:
                if bookmark_created:
                    _save_sharedbookmark(request, bookmark)

            return HttpResponseRedirect(reverse(user_page, args=[request.user.username]))
    else:        
        data = {}
        edit_bookmark = False
        if 'url' or 'id' in request.GET:
            if 'url' in request.GET:
                edit_bookmark = True
                url = request.GET['url']
            else:
                id = request.GET['id']    
            title = ''
            tags = ''
            features = ''
            try:
                if edit_bookmark:
                    link = Link.objects.get(url=url)
                    request.session['link'] = link
                    bookmark = Bookmark.objects.get(
                        link = link,
                        user = request.user
                    )
                    private = bookmark.private
                else:
                    bookmark = Bookmark.objects.get(pk=id)
                    request.session['link'] = bookmark.link
                    private = True 
                title = bookmark.title
                tags = ','.join(tag.name for tag in bookmark.tags.all())
                features = bookmark.features.values_list('id', flat=True)
            except (Link.DoesNotExist, Bookmark.DoesNotExist):
                pass
            data = {
                'title': title,
                'tags': tags,
                'features': features,
                'private': private
            }

        # elif 'id' in request.GET:
        #     id = request.GET['id']
        #     title = ''
        #     tags = ''
        #     features = ''
        #     try:
        #         bookmark = Bookmark.objects.get(pk=id)
        #         request.session['link'] = bookmark.link
        #         title = bookmark.title
        #         tags = ','.join(tag.name for tag in bookmark.tags.all())
        #         features = bookmark.features.values_list('id', flat=True)
        #         private = True
        #         #assert False
        #     except (Bookmark.DoesNotExist):
        #         pass
        #     data = {
        #         'title': title,
        #         'tags': tags,
        #         'features': features,
        #         'private': private
        #     }            
        else:
            link = request.session.get('link', None) 
            if link:
                # driver = webdriver.Firefox()
                # driver.get(link.url)
                # title = driver.title
                # data = {'title': title}
                soup = BeautifulSoup(urllib.urlopen(link.url), "lxml")
                data = {'title': soup.title.string}                
                          
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
    bookmarks = Bookmark.objects.filter(tags__name=tag.name)
    shared_bookmarks = SharedBookmark.objects.filter(bookmark__in=bookmarks)
    variables = {
        'shared_bookmarks': shared_bookmarks, 
        'tag_name': tag.name,
        'show_tags': True, 
        'show_user': True
    }
    return render(request, 'tag_page.html', variables)


def _bookmark_save(request, form):
    bookmark, bookmark_created = Bookmark.objects.get_or_create(
        user=request.user, 
        link=request.session.get('link', None)
    )

    # clean up session
    if 'link' in request.session:
        del request.session['link']

    #Update bookmark title. 
    bookmark.title = form.cleaned_data['title']

    bookmark.private = form.cleaned_data['private']

    # Save bookmark to database.
    bookmark.save()

    if not bookmark_created:
    #     assert False
        bookmark.features.clear()
    # Get features from form
    features = form.cleaned_data['features']

    # Add features to bookmark
    for feature in features:
        bookmark.features.add(feature)

    # Using django-taggit tags added after bookmark is saved
    # Get tags from form
    tags = form.cleaned_data['tags']
    bookmark.tags.set(*tags)


    return bookmark, bookmark_created


def _save_sharedbookmark(request, bookmark):
    interest_poll = SingleChoicePoll.objects.create(
        question = "Interest Poll"
    )                

    # Create poll to report abuse.
    report_abuse_poll = SingleChoicePoll.objects.create(
        question = "Report Abuse Poll"
    )                 

    initial_hot_score = 0

    shared_bookmark = SharedBookmark.objects.create(
        bookmark = bookmark,
        interest_poll = interest_poll,
        report_abuse_poll = report_abuse_poll,
        hot_score = initial_hot_score
    )        

    SingleChoiceVote.objects.create(
        user = request.user, 
        poll = shared_bookmark.interest_poll, 
        ip = get_ip(request)
    )
    shared_bookmark.hot_score = shared_bookmark.get_hot_score()
    shared_bookmark.save()



