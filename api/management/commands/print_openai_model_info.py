from django.core.management.base import BaseCommand, CommandError
from api.models import OpenAIAssistant  # Import UserFile model
import openai

class Command(BaseCommand):
  help = "Print Info about a given model"

  def handle(self, *args, **options):
    try:
      # client = openai.OpenAI()
      # models = OpenAIAssistant.objects.all()
      # for i, model in enumerate(models):
      #   print(f"Processing model {i + 1}/{len(models)}: {model.name} ({model.assistant_id})")
      #   assistant = client.beta.assistants.retrieve(model.assistant_id)
      #   if not assistant:
      #     self.stdout.write(self.style.WARNING(f"Model {model.assistant_id} not found."))
      #     continue
      #   self.stdout.write(self.style.SUCCESS(f"Model Name: {assistant.name}"))
      #   self.stdout.write(self.style.SUCCESS(f"Model Instructions: {assistant.instructions}"))
      #   self.stdout.write(self.style.SUCCESS(f"Model Version: {assistant.model}"))
      #   print(assistant.tools)
      id = OpenAIAssistant.objects.filter(model="gpt-4.1-mini").first().assistant_id
      assistant = openai.beta.assistants.retrieve(id)
      print("Instructions:", assistant.instructions)
        

    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
