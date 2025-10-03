
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('postView/<int:id>/', views.postView, name='postView'),
    path('deletePost/<int:post_id>/', views.deletePost, name='deletePost'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),





    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),



    path('viewProfile/<int:user_id>/', views.viewProfile, name='viewProfile'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('remove_profile_picture/', views.remove_profile_picture, name='remove_profile_picture'),
    path('createPost/', views.createPost, name='createPost'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]