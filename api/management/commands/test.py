from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from api.models import OpenAIThread
from api.utils import create_new_thread_for_user

class Command(BaseCommand):
  help = "Create a new OpenAIThread for a user by username"

  def handle(self, *args, **options):
    try:
      print("Fetching all OpenAI threads...")
      threads = OpenAIThread.objects.all()
      for thread in threads:
        print(f"Thread ID: {thread.thread_id}, Name: {thread.name}, Last Accessed: {thread.last_accessed}")
    except Exception as e:
      raise CommandError(f"An error occurred while fetching threads: {str(e)}")
