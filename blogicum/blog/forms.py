from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма для поста."""

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Форма для комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
