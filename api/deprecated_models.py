from django.db import models
from django.contrib.auth.models import User
import uuid

class Conversation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
  name = models.CharField(max_length=255)  # Name of the conversation
  conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique ID
  last_accessed = models.DateTimeField(auto_now=True)  # Automatically updates to the current timestamp on save

  def __str__(self):
    return self.name