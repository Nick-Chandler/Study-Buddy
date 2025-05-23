from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from api.utils import create_new_thread_for_user

class Command(BaseCommand):
  help = "Create a new OpenAIThread for a user by username"

  def add_arguments(self, parser):
    parser.add_argument("username", type=str, help="The username of the user")
    parser.add_argument("thread_name", type=str, help="The name of the new thread")

  def handle(self, *args, **options):
    username = options["username"]
    thread_name = options["thread_name"]

    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      raise CommandError(f"User with username '{username}' does not exist.")

    thread_id = create_new_thread_for_user(user.id, thread_name)

    if thread_id:
      self.stdout.write(self.style.SUCCESS(f"Created thread '{thread_name}' with ID: {thread_id}"))
    else:
      self.stdout.write(self.style.ERROR("Failed to create thread."))
