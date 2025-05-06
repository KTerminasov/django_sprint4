from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, ProfileChangeForm
from .models import Category, Post
from .utils import get_item, get_post_list

User = get_user_model()


def get_index(request):
    """Просмотр главной страницы."""
    template = 'blog/index.html'
    post_list = get_post_list(filtrate=True)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, template, context)


def get_post_detail(request, post_id):
    """Просмотр детальной информации о посте."""
    post = get_item(Post, post_id, request.user)
    comments = post.comments.select_related('author')
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    template = 'blog/detail.html'
    return render(request, template, context)


def get_category_posts(request, category_slug):
    """Просмотр постов, привязанных к категории."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    # post_list = category.posts.all().filter(
    #     is_published=True,
    #     pub_date__lte=datetime.now()
    # )
    post_list = get_post_list(filtrate=True).filter(category=category_slug)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page_number')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }

    return render(request, template, context)


def view_profile(request, username):
    """Просмотр профиля пользователя."""
    template = 'blog/profile.html'
    user_profile = get_object_or_404(
        User,
        username=username
    )
    post_list = get_post_list(
        filtrate=(request.user == user_profile)
    ).filter(author=user_profile)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user_profile,
        'page_obj': page_obj
    }

    return render(request, template, context)


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя."""
    template = 'blog/user.html'

    form = ProfileChangeForm(request.POST or None, instance=request.user)
    context = {
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, template, context)


@login_required
def create_post(request):
    """Создание поста."""
    template = 'blog/create.html'

    form = PostForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    template = 'blog/create.html'
    post = get_item(Post, post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    context = {'form': form}

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, template, context)


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

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance)
    context = {'form': form}

    if form.is_valid():
        post = form.save(commit=False)
        if post_id is None:
            post.author = request.user
            post.pub_date = timezone.now()
        form.save()

        if post_id is None:
            return redirect('blog:profile', username=request.user.username)
        else:
            return redirect('blog:post_detail', post_id=post_id)

    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    """Удаление поста."""
    template = 'blog/create.html'

    post = get_post(post_id, request.user)
    form = PostForm(instance=post)
    context = {'form': form}

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)

    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """Создание комментария."""
    post = get_post(post_id, request.user)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    template = 'blog/comment.html'

    comment = get_comment(comment_id, request.user)
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'comment': comment,
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)

    return render(request, template, context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    template = 'blog/comment.html'

    comment = get_comment(comment_id, request.user)
    form = CommentForm(instance=comment)
    context = {
        'comment': comment,
        'form': form
    }

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, template, context)
