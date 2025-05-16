from django.test import TestCase

# Create your tests here.
from api.models import Conversation
from django.contrib.auth.models import User

# Get the user who owns the conversation
user = User.objects.get(username="nickc")

# Create a new conversation
conversation = Conversation.objects.create(user=user, name="Study Session")
print(conversation.conversation_id)  # Outputs the unique UUID