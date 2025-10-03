from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.chatList, name='chatList'),
    path('createConversation/<int:user_id>/', views.createConversation, name='createConversation'),

    path('conversation/<int:chat_id>/', views.conversationView, name='conversationView'),
]