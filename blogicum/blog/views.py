from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from datetime import datetime

from django.core.paginator import Paginator
from django.utils import timezone

from .forms import PostForm, CommentForm, ProfileChangeForm

from django.contrib.auth.decorators import login_required

from .utils import get_post, get_comment

from django.contrib.auth import get_user_model
User = get_user_model()


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
    post = get_post(post_id, request.user)
    comments = post.comments.select_related('author')
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
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


def view_profile(request, username):
    """Просмотр профиля пользователя."""
    template = 'blog/profile.html'
    user_profile = get_object_or_404(
        User,
        username=username
    )
    if request.user == user_profile:
        post_list = Post.objects.all().filter(
            author=user_profile
        )
    else:
        post_list = Post.objects.all().filter(
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True,
            author=user_profile
        )

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

    user_profile = request.user
    form = ProfileChangeForm(request.POST or None, instance=user_profile)
    context = {
        'form': form
    }

    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=user_profile.username)

    return render(request, template, context)


@login_required
def act_with_post(request, post_id=None):
    """Создание, редактирование или удаление поста."""
    template = 'blog/create.html'

    if post_id is None:
        instance = Post()
        instance.pub_date = timezone.now()
        instance.author = request.user
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
