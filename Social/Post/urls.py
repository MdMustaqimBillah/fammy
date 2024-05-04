from django.urls import path
from . import views

app_name = 'Post'


urlpatterns =[
    path('',views.home, name='home'),
    path('<int:pk>/', views.home, name='home_like'),
    path('posting/', views.PostMaking.as_view(), name='posting'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view(), name='update_post'),
    path('delete_post/<int:pk>/', views.PostDelete.as_view(), name='delete_post'),
    path('like_post/<int:pk>/', views.liked, name='liked'),
    path('undo_like/<int:pk>/', views.undo_like, name='undo_like'),
    path('comment/<int:pk>/', views.comment_on_post, name='comment'),
    path('edit_comment/<int:pk>/', views.CommentEdit.as_view(), name='edit_comment'),
    path('delete_comment/<int:pk>/', views.CommentDelete.as_view(), name='delete_comment'),
    path('inside_like/<int:pk>/', views.inside_liked, name='inside_liked'),
    path('undo_inside_like/<int:pk>/', views.undo_inside_like, name='undo_inside_like'),
    path('comment_reaction/<int:pk>/', views.comment_reaction, name='comment_reaction'),
    path('undo_comment_reaction/<int:pk>/', views.undo_comment_reaction, name='undo_comment_reaction'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('author_posts/<int:pk>/', views.author_posts, name='author_posts'),
    path('my_post_like/<int:pk>/', views.my_post_like, name='my_post_like'),
    path('undo_my_post_likr/<int:pk>/', views.undo_my_post_like, name='undo_my_post_like')   
]