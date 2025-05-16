from django.db import models
from django.contrib.auth.models import User
import uuid  # To generate unique conversation IDs

class Conversation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
  name = models.CharField(max_length=255)  # Name of the conversation
  conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique ID

  def __str__(self):
      return self.name

class Message(models.Model):
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
  role = models.CharField(max_length=10, choices=[("human", "Human"), ("ai", "AI")])
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"{self.role}: {self.content[:50]}"
