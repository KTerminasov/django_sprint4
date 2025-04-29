from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Форма для поста."""
    
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }