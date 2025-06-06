from django.core.management.base import BaseCommand
from api.models import OpenAIAssistant
import openai
import os

class Command(BaseCommand):
  help = "Create and store a single OpenAI Assistant"

  def handle(self, *args, **options):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    assistant = openai.beta.assistants.create(
      name="General Knowledge Assistant - 4.1 Mini",
      instructions="You are helpful with general knowledge questions and queries",
      model="gpt-4o-mini",
      tools=[{"type": "file_search"}]
    )
    print(f"New OpenAI Assistant created: {assistant.id}")

    OpenAIAssistant.objects.create(
      assistant_id=assistant.id,
      name=assistant.name,
      instructions=assistant.instructions,
      model=assistant.model
    )

    self.stdout.write(self.style.SUCCESS(f"Assistant Model added created: {assistant.id}"))
