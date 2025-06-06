from django.core.management.base import BaseCommand
from api.models import OpenAIAssistant
from api.utils import print_costs_for_all_models
import openai, time


class Command(BaseCommand):
  help = "Send a prompt and PDF to the GPT Assistant API"

  def handle(self, *args, **options):
    OpenAIAssistant.objects.all()
    for assistant in assistants:
      print(f" - {assistant.name} ({assistant.model})")