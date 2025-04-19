from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from datetime import datetime


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.all().filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )
    context = {'post': post}
    template = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.all().filter(
        is_published=True,
        pub_date__lte=datetime.now()
    )
    context = {
        'category': category,
        'post_list': post_list
    }

    return render(request, template, context)
