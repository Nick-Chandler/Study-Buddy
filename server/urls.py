"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("assistant/<int:user_id>/<str:thread_id>", views.assistant, name="assistant"),
    path("get_user_thread_list/<int:user_id>", views.get_user_thread_list, name="get_user_thread_list"),
    path("get_user_thread_messages/<int:user_id>/<str:thread_id>", views.get_user_thread_messages, name="get_user_thread_messages"),
    path('create_thread_for_user/<int:user_id>/<str:name>', views.create_thread_for_user, name='create_thread_for_user'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('conversation/<str:cid>/', views.conversation_view, name='conversation'),
    path('conversationlist/', views.ConversationListView.as_view(), name='conversation-list'),
    path('threads/', views.OpenAIThreadListView.as_view(), name='thread-list'),
]
