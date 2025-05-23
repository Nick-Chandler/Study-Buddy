from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid  # To generate unique conversation IDs

class Conversation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
  name = models.CharField(max_length=255)  # Name of the conversation
  conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique ID
  last_accessed = models.DateTimeField(auto_now=True)  # Automatically updates to the current timestamp on save

  def __str__(self):
      return self.name

class Message(models.Model):
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
  role = models.CharField(max_length=10, choices=[("human", "Human"), ("ai", "AI")])
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"{self.role}: {self.content[:50]}"
  
from django.db import models

class OpenAIAssistant(models.Model):
  assistant_id = models.CharField(max_length=100, unique=True)
  name = models.CharField(max_length=100)
  instructions = models.TextField()
  model = models.CharField(max_length=50, default="gpt-4o")
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} ({self.assistant_id})"
  
class OpenAIThread(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='openai_threads')
  thread_id = models.CharField(max_length=100, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_accessed = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"Thread for {self.user.username}: {self.thread_id}"

