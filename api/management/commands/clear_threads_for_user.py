from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
  help = "Clear All Threads for a User"

  def add_arguments(self, parser):
    parser.add_argument("username", type=str, help="The username of the user")

  def handle(self, *args, **options):
    username = options["username"]

    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      raise CommandError(f"User with username '{username}' does not exist.")

    for thread in User.objects.get(username=username).openai_threads.all():
      thread.delete()
      self.stdout.write(self.style.SUCCESS(f"Deleted thread: {thread.name}"))


