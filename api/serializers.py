from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, OpenAIAssistant, OpenAIThread, UserFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Excludes sensitive field 'password'

class OpenAIThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenAIThread
        fields = ['user', 'name', 'thread_id', 'created_at', 'last_accessed']  # Include all fields

class UserFileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserFile
        fields = ['id', 'user','username','filename', 'last_accessed']  # Assuming user_files is a related name for UserFiles model