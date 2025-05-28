from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message, OpenAIAssistant, OpenAIThread, UserFile

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'timestamp']  # Include the fields you want to expose

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Nested serializer for messages

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'conversation_id', 'user', 'messages']  # Include messages in the output

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