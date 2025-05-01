from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404


def get_post(post_id, user, redirect=None):
    """Получение объекта поста по post_id с проверкой авторства."""
    post = get_object_or_404(
        Post,
        pk=post_id,
    )

    if post.author != user:
        if (post.pub_date > timezone.now()
                or post.is_published is False
                or post.category.is_published is False):
            raise Http404()

    return post


def get_comment(comment_id, user):
    """Получение объекта комментария по comment_id."""
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        author=user
    )
    return comment
