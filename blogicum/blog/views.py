from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()

from django.core.paginator import Paginator

from .forms import PostForm

from django.contrib.auth.decorators import login_required

def index(request):
    """View-функция главной страницы."""
    template = 'blog/index.html'
    post_list = Post.objects.all().filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
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

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page_number')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }

    return render(request, template, context)


def user_detail(request, username):
    """View-функция страницы пользователя."""
    template = 'blog/profile.html'
    profile = get_object_or_404(
        User,
        username=username
    )
    post_list = Post.objects.all().filter(
        author = profile
    )

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj':page_obj
    }

    return render(request, template, context)

def user_edit(context):
    return context

@login_required
def act_with_post(request, post_id=None):
    """Создание, редактирование или удаление поста."""
    template = 'blog/create.html'
    
    if post_id is None:
        instance = None
    else:
        instance = get_object_or_404(Post, pk=post_id)
        if request.user != instance.author:
            return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form }
    
    if form.is_valid():
        form.save() 
        if post_id == None:      
            return redirect('blog:detail', username=request.user.username)
        else:
            return redirect('blog:post_detail', post_id=post_id)
    
    return render(request, template, context)

def page_not_found(request, exception):
    """Обработка ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Обработка ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def internal_server_error(request):
    """Обработка ошибки 500."""
    return render(request, 'pages/500.html', status=500)
