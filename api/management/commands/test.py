from django.core.management.base import BaseCommand
from api.models import OpenAIThread, User


class Command(BaseCommand):
  help = "Send a prompt and PDF to the GPT Assistant API"

  def handle(self, *args, **options):
    user = User.objects.get(id=1)  # Replace with actual user ID or logic to get user
    for thread in OpenAIThread.objects.filter(user=user):
      print(f"Thread ID: {thread.thread_id}, Thread Name: {thread.name}")
    