from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import BlogPost, Notification, Space, Comment
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, CreateSpaceForm, CreateCommentForm
from account.models import Account
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter

POSTS_PER_PAGE = 10

def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')
    
    form = CreateBlogPostForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = user
        obj.author = author
        obj.save()
        return redirect('home')
    else:
        print("asdasdasd")
    context['form'] = form


    return render(request, 'blog/create_post.html', context)


def delete_post_view(request,slug):
    post = BlogPost.objects.get(slug=slug)
    post.delete()

    return redirect('home')

def create_space_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')
    
    form = CreateSpaceForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('home')
    

    context['form'] = form

    return render(request, 'blog/create_space.html', context)


def detail_post_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    likes_count = blog_post.total_likes
    unlikes_count = blog_post.total_unlikes
    context['blog_post'] = blog_post
    context['likes_count'] = likes_count
    context['unlikes_count'] = unlikes_count

    return render(request, 'blog/detail_post.html', context)


def edit_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse("<h1 class='display-2'>You are not the author of that post.</h1>")

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Successfully Updated"
            blog_post = obj
            return redirect('detail-post', blog_post.slug)

    form = UpdateBlogPostForm(
        initial= {
            "title" : blog_post.title,
            "body" : blog_post.body,
            "category" : blog_post.category,
            "space" : blog_post.space,
            "post_type" : blog_post.post_type
        }
    )            

    context['form'] = form
    return render(request, 'blog/edit_post.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__icontains=q),
            Q(body__icontains=q),
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def like_post_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    post.likes.add(request.user)
    post.unlikes.remove(request.user)

    note = Notification()
    note.notification_type = 1
    note.to_user = post.author
    note.from_user = request.user
    note.post = post
    note.save()
    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def remove_like_post_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def unlike_post_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    post.likes.remove(request.user)
    post.unlikes.add(request.user)

    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def remove_unlike_post_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    post.unlikes.remove(request.user)

    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def show_category_page_view(request, category_name):
    context = {}
    
    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')

    spaces = Space.objects.all().filter(category__name = category_name)

    context['spaces'] = spaces
    context['category_name'] = category_name

    return render(request, 'blog/category_page.html', context)


def show_space_page_view(request, space_name):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    posts = BlogPost.objects.all().filter(space__name = space_name)
    
    # Pagination
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, POSTS_PER_PAGE)

    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context['posts'] = posts
    context['space_name'] = space_name

    return render(request, 'blog/space_page.html', context)


def create_comment_view(request,slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    
    form = CreateCommentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.get(email=user.email)
        obj.author = author
        obj.post = post
        obj.save()

        note = Notification()
        note.notification_type = 2
        note.to_user = post.author
        note.from_user = user
        note.post = post
        note.save()

        return redirect('detail-post', slug)
    
    form = CreateCommentForm(
        initial= {
            "author" : user,
            "post" : post
        }
    ) 

    context['form'] = form


    return render(request, 'blog/create_comment.html', context)


def like_comment_view(request, slug, comment_id):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likes.add(request.user)
    comment.unlikes.remove(request.user)

    note = Notification()
    note.notification_type = 1
    note.to_user = comment.author
    note.from_user = request.user
    note.comment = comment
    note.save()

    return redirect('detail-post', slug)


def unlike_comment_view(request,slug, comment_id):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likes.remove(request.user)
    comment.unlikes.add(request.user)

    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def remove_like_comment_view(request,slug, comment_id):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likes.remove(request.user)
    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def remove_unlike_comment_view(request, slug, comment_id):
    if not request.user.is_authenticated:
        return redirect('must-authenticate')
    
    post = get_object_or_404(BlogPost, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.unlikes.remove(request.user)

    return HttpResponseRedirect(reverse('detail-post', args=[str(slug)]))


def post_notification(request, notification_pk, post_pk):
    context = {}

    notification = Notification.objects.get(pk=notification_pk)
    post = BlogPost.objects.get(pk=post_pk)

    notification.user_has_seen = True
    notification.save()

    return redirect('detail-post', post.slug)



