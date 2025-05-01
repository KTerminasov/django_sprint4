from .models import Post
from django.shortcuts import get_object_or_404
from datetime import datetime


def get_post(post_id):
    """Получение объекта поста по post_id."""
    post = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )
    return post
