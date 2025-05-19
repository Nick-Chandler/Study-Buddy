from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message

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