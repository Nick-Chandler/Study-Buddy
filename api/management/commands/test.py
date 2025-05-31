from django.core.management.base import BaseCommand, CommandError
from api.models import OpenAIThread, UserFile  # Import UserFile model
from api.utils import create_new_thread_for_user

class Command(BaseCommand):
  help = "Delete all UserFile objects for a specific user by username"

  def handle(self, *args, **options):
    try:
      username = "nickc"  # Specify the username
      user_files = UserFile.objects.filter(user__username=username)
      count = user_files.count()
      user_files.delete()
      self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} UserFile objects for user '{username}'."))
    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
