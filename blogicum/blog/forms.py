from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма для поста."""

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Форма для комментария."""

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileChangeForm(forms.ModelForm):
    """Форма для изменения профиля пользователя."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
