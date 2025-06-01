from django.core.management.base import BaseCommand, CommandError
from api.models import User, UserFile  # Import UserFile model
from api.utils import create_new_thread_for_user

class Command(BaseCommand):
  help = "Delete all UserFile objects for a specific user by username"

  def handle(self, *args, **options):
    try:
      users = User.objects.all()
      for user in users:
        print(f"User: {user.username}, ID: {user.id}")
    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
