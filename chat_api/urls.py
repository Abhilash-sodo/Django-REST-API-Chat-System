from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('chat/', views.chat, name='chat'),
    path('balance/', views.token_balance, name='token_balance'),
    # Bonus PATH
    path('users/', views.get_all_users, name='get_all_users'),
    # path('users/<int:user_id>/', views.get_user_detail, name='get_user_detail'),
    # path('users/<int:user_id>/chats/', views.get_user_chat_history, name='get_user_chat_history'),
]