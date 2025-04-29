from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.post_detail, name="post_detail"),
    path('<slug:category_slug>/', views.category_posts,
         name="category_posts"),
    path('profile/edit', views.user_edit, name='edit_profile'),
    path('profile/<str:username>', views.user_detail, name='profile'),
    path('create', views.create_post, name='create_post')
    
]
