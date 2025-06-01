from django.core.management.base import BaseCommand, CommandError
from api.models import User, UserFile  # Import UserFile model
from api.utils import create_new_thread_for_user

class Command(BaseCommand):
  help = "Delete all UserFile objects for a specific user by username"
  def add_arguments(self, parser):
    parser.add_argument("username", type=str, help="The username of the user")

  def handle(self, *args, **options):
    username = options["username"]
    try:
      user = User.objects.get(username=username)
      user_files = UserFile.objects.filter(user=user)
      print(f"Found {user_files.count()} files for user '{username}':")
      for user_file in user_files:
        print(f"User: {user.username}, File: {user_file.filename}, Size: {user_file.file.size} bytes")
    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
