from django.core.management.base import BaseCommand, CommandError
from api.models import OpenAIAssistant  # Import UserFile model
from api.utils import create_new_thread_for_user

class Command(BaseCommand):
  help = "Delete all UserFile objects for a specific user by username"

  def handle(self, *args, **options):
    try:
      OpenAIAssistant.objects.create(
        assistant_id="asst_ceOd9c6y55I9vToqnkJKUnj7",
        name="Homework Assistant",
        instructions="You are a general purpose assistant to help with user queries. You specialize in homework/study help but it is important that you are able to answer general, unrelated questions as well.",
        model="gpt-4o"
      )
      
    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
