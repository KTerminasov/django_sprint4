from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .models import Post


def get_post_list(filtrate=False):
    """Получение списка постов с возможностью фильтрации."""
    post_list = Post.objects.select_related(
        'author', 'category', 'location'
    )

    if filtrate:
        return post_list.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    return post_list


def check_author


def get_item(model, pk, author=None):
    """Получение объекта модели по id."""
    item = get_object_or_404(
        model,
        pk=pk,
    )

    if author is not None:
        if item.author != author:
            return item.filter(
                pub_date__date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            )
    return item



