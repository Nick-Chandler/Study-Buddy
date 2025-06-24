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
    path("assistant/<int:user_id>/<str:thread_id>", views.assistant2, name="assistant2"),
    path("get_user_thread_list/<int:user_id>", views.get_user_thread_list, name="get_user_thread_list"),
    path("get_user_thread_messages/<int:user_id>/<str:thread_id>", views.get_user_thread_messages, name="get_user_thread_messages"),
    path('create_thread_for_user/<int:user_id>/<str:name>', views.create_thread_for_user, name='create_thread_for_user'),
    path('rename_thread/<int:user_id>/<str:thread_id>/<str:new_name>', views.rename_thread, name='rename_thread'),
    path('delete_thread/<int:user_id>/<str:thread_id>', views.delete_thread, name='delete_thread'),
    path('upload_document/<int:user_id>',views.upload_document, name='upload_document'),
    path('login/', views.login_view, name='login'),
    path('firebase_login/<str:email>', views.firebase_login_view, name='firebase_login'),
    path('register/', views.register_view, name='register'),
    path('threads/', views.OpenAIThreadListView.as_view(), name='thread-list'),
    path('all-files/', views.AllUserFilesView.as_view(), name='all-user-files'),
    path('file-url/', views.get_file_url, name='get_file_url'),
    # path('test/', views.test_view, name='test-view'),
]
