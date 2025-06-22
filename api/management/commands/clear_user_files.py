from django.core.management.base import BaseCommand, CommandError
from api.models import User, UserFile  # Import UserFile model

class Command(BaseCommand):
  help = "Delete all UserFile objects for a specific user by username"
  def add_arguments(self, parser):
    parser.add_argument("username", type=str, help="The username of the user")

  def handle(self, *args, **options):
    username = options["username"]
    try:
      print(f"Deleting UserFile objects for user: {user.username} (ID: {user.id})")
      user = User.objects.get(username=username)
      print(f"Found user: {user.username} (ID: {user.id})")
      user_files = UserFile.objects.filter(user=user)
      print(f"Found {user_files.count()} UserFile objects for user '{username}'.")
      count = user_files.count()
      print(f"Deleting {count} UserFile objects...")
      user_files.delete()
      self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} UserFile objects for user '{username}'."))
    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
