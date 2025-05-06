from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.get_index, name='index'),
    path('<int:post_id>/', views.get_post_detail, name="post_detail"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.view_profile, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('<slug:category_slug>/', views.get_category_posts,
         name="category_posts"),
]
