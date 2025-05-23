from django.core.management.base import BaseCommand
from api.models import OpenAIAssistant
import openai
import os

class Command(BaseCommand):
  help = "Create and store a single OpenAI Assistant"

  def handle(self, *args, **options):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if OpenAIAssistant.objects.exists():
      self.stdout.write(self.style.WARNING("Assistant already exists."))
      return

    assistant = openai.beta.assistants.create(
      name="Image & Info Assistant",
      instructions="You are helpful at identifying people in images and answering questions based on images and text.",
      model="gpt-4o",
      tools=[{"type": "file_search"}]
    )

    OpenAIAssistant.objects.create(
      assistant_id=assistant.id,
      name=assistant.name,
      instructions=assistant.instructions,
      model=assistant.model
    )

    self.stdout.write(self.style.SUCCESS(f"Assistant created: {assistant.id}"))
