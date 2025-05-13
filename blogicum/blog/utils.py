from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Post, Comment


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


def get_item(model, pk, author):
    """Получение объекта модели по id."""
    item = get_object_or_404(
        model,
        pk=pk,
    )

    if item.author != author:
        if model == Comment or (item.pub_date > timezone.now()
                                or item.is_published is False
                                or item.category.is_published is False):
            raise Http404
    return item
