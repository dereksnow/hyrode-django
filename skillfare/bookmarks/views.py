import urllib
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from spynner import Browser
from pyquery import PyQuery

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from bookmarks.models import SharedBookmark, Bookmark, Link, Path, SharedPath, LikeVote, AbuseVote, LevelVote
from bookmarks.forms import BookmarkSaveForm, LinkSaveForm, PathSaveForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from taggit.models import Tag
from django.views.generic import DetailView
from bookmarks.models import Bookmark, SharedBookmark
from bookmarks.utils import get_ip
from itertools import chain
from operator import attrgetter
from django.db.models import Count
import HTMLParser

from django.contrib.contenttypes.models import ContentType


def bookmark_detail(request, pk, slug = ''):
    bookmark = get_object_or_404(Bookmark, pk = pk)
    if bookmark.slug != slug:
        return HttpResponseRedirect(reverse(bookmark_detail, args=[pk, bookmark.slug]))
    variables = {'bookmark': bookmark,
                 'hide_more': True}
    return render(request, 'detail.html', variables)

def path_detail(request, pk, slug = ''):
    path = get_object_or_404(Path, pk = pk)
    if path.slug != slug:
        return HttpResponseRedirect(reverse(path_detail, args=[pk, path.slug]))

    bookmarks = Bookmark.objects.filter(pk__in = path.bookmarks.all)
    variables = {'bookmarks': bookmarks}
    return render(request, 'bookmark_list.html', variables)

def shared_bookmark_detail(request, pk, slug = ''):
    shared_bookmark = get_object_or_404(SharedBookmark, pk = pk)
    if shared_bookmark.bookmark.slug != slug:
        return HttpResponseRedirect(
            reverse(shared_bookmark_detail, args=[pk, shared_bookmark.slug])
        )
    variables = {'bookmark': shared_bookmark.bookmark,
                 'hide_more': True}
    return render(request, 'detail.html', variables)

def main_page(request):
    shared_bookmarks = SharedBookmark.objects.all()
    shared_paths = SharedPath.objects.all()
    resources = sorted(chain(shared_bookmarks, shared_paths), key=attrgetter('created'), reverse=False)
    variables = {
        # 'bookmarks': shared_bookmarks,
        'resources': resources,
        'show_tags': True,
        'show_user': True,
        'no_form_container': True
    }
    return render(request, 'main_page.html', variables)

def search(request):
    if request.method == 'GET':
        if 'query' in request.GET:
            query = request.GET['query'].strip()
            if query:     

                shared_bookmarks = SharedBookmark.objects.search(query)
                shared_paths = SharedPath.objects.search(query)
                tag_query = query.split()
                tagged_shared_bookmarks = SharedBookmark.objects.filter(bookmark__tags__name__in = tag_query).distinct()
                tagged_shared_paths = SharedPath.objects.filter(path__tags__name__in = tag_query).distinct()

                
                resources = chain(shared_bookmarks, shared_paths, tagged_shared_bookmarks, tagged_shared_paths)
                variables = {        
                    'resources': resources,
                    'show_tags': True,
                    'show_user': True,
                    'palette': True
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
                    if bookmark.personal == True or (bookmark.personal == False and 
                        bookmark.sharedbookmark.interest_poll.count_votes() < 2):
                        bookmark.delete()

            elif operation == 'private':
                for bookmark in bookmark_list:
                    if bookmark.sharedbookmark.interest_poll.count_votes() < 2:
                        bookmark.sharedbookmark.delete()
                        bookmark.personal = True

            elif operation == 'public':                
                for bookmark in bookmark_list:
                    _save_sharedbookmark(reqest, bookmark)
                bookmark_list.update(personal=False)                    

            #return HttpResponseRedirect('/user/%s/' % request.user.username)    
        return HttpResponseRedirect(reverse(user_page, args=[request.user.username]))    
    else:        
        show_edit = request.REQUEST.get('show_edit', False) and request.user.username == username
        user = get_object_or_404(User, username=username)

        personal_bookmark = None
        personal_paths = None
        shared_bookmarks = SharedBookmark.objects.filter(bookmark__user = user)
        shared_paths = SharedPath.objects.filter(path__user = user)

        if request.user.username == username:
            personal_bookmarks = Bookmark.objects.filter(user = user, personal = True)
            personal_paths = Path.objects.filter(user = user, personal = True)
        
        #bookmarks = user.bookmark_set.order_by('-id')
        variables = {
            'username': username, 
            'shared_bookmarks': shared_bookmarks, 
            'shared_paths': shared_paths,
            'show_edit': show_edit,
            'show_single_edit': user == request.user
        }

        return render(request, 'user_page.html', variables)

@login_required
def create_path(request, username):
    user = get_object_or_404(User, username=username)
    # if user != request.user:
    #     raise Http404


    shared_bookmarks = SharedBookmark.objects.filter(bookmark__user = user)

    # if request.user.username == username:
    #     personal_bookmarks = Bookmark.objects.filter(user = user, personal = True)    

    variables = {
        'shared_bookmarks': shared_bookmarks, 
        'path': True
    }
    # Explicit set personal_bookmarks and personal_paths to None
    # for other users   s 
    # variables.setdefault(personal_bookmarks, None)
    return render(request, 'path_create.html', variables)

@login_required
def delete_bookmark(request, pk):
    redirect_to = request.REQUEST.get('next', '')
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if bookmark.personal == True:
        bookmark.delete()
    else:
        shared = get_object_or_404(SharedBookmark, bookmark=bookmark) 
        if shared.interest_poll.count_votes() < 3:
            bookmark.delete()
        else:
            pass
            # assign another user to bookmark???
    return HttpResponseRedirect(redirect_to)


@login_required
def interest_vote(request, pk, model):

    redirect_to = request.REQUEST.get('next', '')   
    print model
    print pk 
    resource = get_object_or_404(model, pk=pk)   
    resource_type = ContentType.objects.get_for_model(resource)    

    ip = get_ip(request)

    # if UserVote.objects.filter(shared_bookmark = shared_bookmark, ip = ip).count() < 5:            
    if LikeVote.objects.filter(ip = ip, content_type__pk = resource_type.id, object_id = resource.id).count() < 5:        
        try:        
            # UserVote.objects.get(user = request.user, shared_bookmark = shared_bookmark)        
            LikeVote.objects.get(user = request.user, content_type__pk = resource_type.id, object_id = resource.id)            
            if request.is_ajax():                
                return HttpResponse(-1)
        except LikeVote.DoesNotExist:            
            # UserVote.objects.create(user = request.user, ip = ip, shared_bookmark = shared_bookmark)
            LikeVote.objects.create(content_object = resource, user = request.user, ip = ip)
            if request.is_ajax():
                return HttpResponse(resource.like_votes.count())

    return HttpResponseRedirect(redirect_to)


@login_required
def report_abuse_vote(request, pk, model):
    redirect_to = request.REQUEST.get('next', '')

    resource = get_object_or_404(model, pk=pk)
    resource_type = ContentType.objects.get_for_model(resource)

    ip = get_ip(request)

    #if SingleChoiceVote.objects.filter(poll = shared_bookmark.report_abuse_poll, ip = ip).count() <= 5:
    if AbuseVote.objects.filter(ip = ip, content_type__pk = resource_type.id, object_id = resource.id).count() < 5:
        try:
            #SingleChoiceVote.objects.get(user = request.user, poll = shared_bookmark.report_abuse_poll)
            print u' abuse votes %s ' % (resource.abuse_votes.count())   
            print u' like votes %s ' % (resource.like_votes.count())              
            AbuseVote.objects.get(user = request.user, content_type__pk = resource_type.id, object_id = resource.id)
        except AbuseVote.DoesNotExist: 
            if resource.abuse_votes.count() < 5:
                AbuseVote.objects.create(content_object = resource, user = request.user, ip = ip)
                if request.is_ajax():
                    return HttpResponse(resource.abuse_votes.count())
            else :
                resource.bookmark.delete()                
                            
    print u' abuse votes %s ' % (resource.abuse_votes.count())   
    print u' like votes %s ' % (resource.like_votes.count()) 
    return HttpResponseRedirect(redirect_to)




@login_required
def level_vote(request, pk, level):
    redirect_to = request.REQUEST.get('next', '')
    
    link = get_object_or_404(Link, pk=pk)

    ip = get_ip(request)

    if LevelVote.objects.filter(link = link, ip=ip).count() <= 5:        
        try:        
            LevelVote.objects.get(user = request.user, link = link)
            if request.is_ajax():
                return HttpResponse(-1)
        except LevelVote.DoesNotExist:
            LevelVote.objects.create(user = request.user, ip = ip, learn_level = level, link = link)
            if request.is_ajax():
                if level == 'BR':
                    count = link.count_beginner_votes()
                elif level == 'IN':
                    count = link.count_intermediate_votes()
                elif level == 'AD':
                    count = link.count_advanced_votes()
                else:
                    raise Http404 

                return HttpResponse(count)


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
                link = Link.objects.create(
                    url = form.cleaned_data['url']
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
                        
            if not form.cleaned_data['personal']:
                # create a shared_bookmark for newly created public bookmark
                if bookmark_created:
                    _save_sharedbookmark(request, bookmark)
                    
                # This case is for a bookmark having been marked as private and
                # then made public                 
                else:
                    try:
                        SharedBookmark.objects.get(bookmark = bookmark)
                    except SharedBookmark.DoesNotExist:
                        _save_sharedbookmark(request, bookmark)  
                
                bookmark.personal = False 
            # bookmark is personal
            else: 
                # check if a personal bookmark has an existing shared_bookmark
                # and remove it. This case is for a bookmark having been
                # marked as public and then made private
                if not bookmark_created:
                    try:
                        shared = SharedBookmark.objects.get(bookmark = bookmark)
                        if shared.like_votes.count() < 4:
                            shared.delete()
                            # need to possibly add return value here to indicate
                            # successful removal
                        else:
                            pass
                            # need to possibly add return value here to indicate
                            # that the bookmark has too many likes to remove                                                        
                    except SharedBookmark.DoesNotExist:
                        pass
                # else bookmark just created 
                    # no need to check for existing SharedBookmark, since
                    # bookmark was just created

                bookmark.personal = True
                                          
            if request.is_ajax():
                variables = {
                    'bookmarks': [bookmark],
                    'show_single_edit': True,
                    'show_tags': True
                }
                return render(request, 'bookmark_list.html', variables)
            else:
                return HttpResponseRedirect(reverse(user_page, args=[request.user.username]))
        else:
            if request.ajax():
                return HttpResponse('failure')                
    else:     
        data = {}
        edit_bookmark = False
        if 'url' in request.GET or 'id' in request.GET:            
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
                    personal = bookmark.personal
                else:
                    bookmark = Bookmark.objects.get(pk=id)
                    request.session['link'] = bookmark.link
                    personal = True 
                title = bookmark.title
                tags = ','.join(tag.name for tag in bookmark.tags.all())
                features = bookmark.features.values_list('id', flat=True)
            except (Link.DoesNotExist, Bookmark.DoesNotExist):
                pass
            data = {
                'title': title,
                'tags': tags,
                'features': features,
                'personal': personal
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
        #         personal = True
        #         #assert False
        #     except (Bookmark.DoesNotExist):
        #         pass
        #     data = {
        #         'title': title,
        #         'tags': tags,
        #         'features': features,
        #         'personal': personal
        #     }            
        else:
            link = request.session.get('link', None) 
            if link:
                #################################################
                # Look at possibly using phantomjs to get title
                ##################################################
                # driver = webdriver.Firefox()
                # driver.get(link.url)
                # title = driver.title
                # data = {'title': title}
                soup = BeautifulSoup(urllib.urlopen(link.url), "lxml")
                data = {'title': soup.title.string}                
                          
        form = BookmarkSaveForm(initial=data)
    variables = {'form': form}
    if request.is_ajax():
        return render(request, 'bookmark_save_form.html', variables)
    else:
        return render(request, 'bookmark_save.html', variables)

@login_required
def path_save(request):
    # if user != request.user.username:
    #     raise PermissionDenied
    if request.method == 'POST':
        form = PathSaveForm(request.POST)
        if form.is_valid():
            path, path_created = _path_save(request, form)

            if not form.cleaned_data['personal']:

               # retrieve list of personal bookmarks
                personal_bookmarks = Bookmark.objects.filter(pk__in = request.session['ids_list'], personal=True)

                # clean up session
                if 'ids_list' in request.session:
                    del request.session['ids_list']

                # if path is public, then bookmarks in path
                # need to be visible to all. Ensure warning to user
                # upon creating a public path that contains personal 
                # bookmarks  
                for bookmark in personal_bookmarks:
                    try:
                        SharedBookmark.objects.get(bookmark = bookmark)
                    except SharedBookmark.DoesNotExist:
                        _save_sharedbookmark(request, bookmark)                

                # create a shared_path for newly created public path
                if path_created:
                    _save_sharedpath(request, path)

                # This case is for a path having been marked as private and
                # then made public
                else:
                    try:
                        SharedPath.objects.get(path = path)
                    except SharedPath.DoesNotExist:
                        _save_sharedpath(request, path)

                path.personal = False

            # path is personal
            else:
                # check if a personal path has an existing shared_path
                # and remove it. This case is for a path having been
                # marked as public and then made private                
                if not path_created:
                    try:
                        shared = SharedPath.objects.get(path = path)
                        if shared.like_votes.count < 4:
                            shared.delete()
                            # need to possibly add return value here to indicate
                            # successful removal
                        else:
                            pass
                            # need to possibly add return value here to indicate
                            # that the bookmark has too many likes to remove 
                    except SharedPath.DoesNotExist:
                        pass
                # else path just created
                    # no need to check for existing SharedPath, since 
                    # path was just created                              

                path.personal = True

            return HttpResponseRedirect(reverse(user_page, args=[request.user.username]))
        
    else:     
        data = {}
        if 'edit' in request.GET or 'ids' in request.GET:
            if 'edit' in request.GET:
                edit_path = True
                edit_id = request.GET['edit']
                path = get_object_or_404(Path, pk=edit_id)
                title = path.title
                features = path.features    
                tags = path.tags

            else:                                      
                ids_list = request.GET['ids'].split(",")
                request.session['ids_list'] = ids_list
            
            # get tags and features for all bookmarks
            tag_list = []
            feature_list = []
            for id in ids_list:
                bookmark = Bookmark.objects.get(pk=id)
                tag_list.append(','.join(tag.name for tag in bookmark.tags.all()))
                feature_list.append(bookmark.features.values_list('id', flat=True))
            tags = ','.join(tag_list)

            # use set to remove redundant tags/features
            tags = ', '.join(sorted(set(tags.split(','))))

            features = []
            # feature_list is actually a ValuesListQuerySet, so iterate
            # through list and convert to string before join
            for l in feature_list:
                features += l
            features = ','.join(set((str(feature) for feature in features)))
            
            data = {
                'tags': tags,
                'features': features
            }

            form = PathSaveForm(initial=data)

            variables = {'form': form}
            return render(request, 'path_save.html', variables)
            
def _path_save(request, form):
    ids = request.session.get('ids_list', None)

    path_created = False
    query_set = Path.objects.filter(user = request.user)
    query_set = query_set.annotate(count=Count('bookmarks')).filter(count=len(ids))
    for _id in ids:
        query_set = query_set.filter(bookmarks__id=_id)

    if query_set:
        path = query_set[0]
        print path
    else:
        path = Path.objects.create(user = request.user)
        path_created = True

    bookmarks = Bookmark.objects.filter(pk__in = ids)
    #Update path title.
    path.title = form.cleaned_data['title']

    path.personal = form.cleaned_data['personal']

    # Save path to database.
    path.save()

    path.bookmarks.add(*bookmarks)

    # Get features from form
    features = form.cleaned_data['features']

    #Add features to path
    path.features.add(*features)
    # for feature in features:
    #     path.features.add(feature)

    # Using django-taggit tags added after path is saved
    # Get tags from form
    tags = form.cleaned_data['tags']
    path.tags.set(*tags)

    return path, path_created

def _save_sharedpath(request, path):

    initial_hot_score = 0

    shared_path = SharedPath.objects.create(
        path = path,
        s_title = path.title,
        hot_score = initial_hot_score
    )

    ip = get_ip(request)

    LikeVote.objects.create(content_object = shared_path, user = request.user, ip = ip)

    shared_path.hot_score = shared_path.get_hot_score()
    shared_path.save()
                
def tag_page(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)

    shared_bookmarks = SharedBookmark.objects.filter(bookmark__tags__name=tag.name)
    shared_paths = SharedPath.objects.filter(path__tags__name=tag.name)
    resources = sorted(chain(shared_bookmarks, shared_paths), key=attrgetter('created'), reverse=False)
    variables = {
        'resources': resources, 
        'tag_name': tag.name,
        'show_tags': True, 
        'show_user': True,
        'palette': True
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

    bookmark.personal = form.cleaned_data['personal']

    # Save bookmark to database.
    bookmark.save()

    if not bookmark_created:
    #     assert False
        bookmark.features.clear()
    # Get features from form
    features = form.cleaned_data['features']

    # Add features to bookmark
    bookmark.features.add(*features)
    # for feature in features:
    #     bookmark.features.add(feature)

    # Using django-taggit tags added after bookmark is saved
    # Get tags from form
    tags = form.cleaned_data['tags']
    bookmark.tags.set(*tags)

    return bookmark, bookmark_created


def _save_sharedbookmark(request, bookmark):
            
    initial_hot_score = 0

    shared_bookmark = SharedBookmark.objects.create(
        bookmark = bookmark,
        s_title = bookmark.title,
        # interest_poll = interest_poll,
        # report_abuse_poll = report_abuse_poll,
        hot_score = initial_hot_score
    )        

    # LikeVote.objects.create(
    #     user = request.user,
    #     ip = get_ip(request),
    #     shared_bookmark = shared_bookmark
    # )

    ip = get_ip(request)

    LikeVote.objects.create(content_object = shared_bookmark, user = request.user, ip = ip)

    #Sshared_bookmark.hot_score = shared_bookmark.get_hot_score()
    shared_bookmark.save()



