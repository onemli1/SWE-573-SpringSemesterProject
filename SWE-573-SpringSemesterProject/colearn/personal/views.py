from operator import attrgetter
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.models import BlogPost, Category, Space
from blog.views import get_blog_queryset


POSTS_PER_PAGE = 10

def home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    categories = Category.objects.all()

    context['categories'] =categories

    return render(request, 'personal/home.html', context)