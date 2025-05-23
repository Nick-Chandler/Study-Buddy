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
from api.views import assistant, login_view, register_view, ConversationListView, conversation_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("assistant/<str:cid>", assistant, name="assistant"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('conversation/<str:cid>/', conversation_view, name='conversation'),
    path('conversationlist/', ConversationListView.as_view(), name='conversation-list'),
]
