from django.urls import path
from Authentication import views


app_name = 'Authentication'


urlpatterns =[
    path('<int:pk>/', views.user_login, name='user_login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_details_form/', views.update_profile, name='user_details_form'),
    path('profile/', views.profile, name='profile'),
    path('password_change/', views.password_change, name='password_change'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('author_profile/<int:pk>', views.author_profile, name='author_profile'),
    path('delete_account/<int:pk>', views.AccountDelete.as_view(), name='delete_account'),
]