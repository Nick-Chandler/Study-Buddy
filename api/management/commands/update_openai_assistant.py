from django.core.management.base import BaseCommand
import openai
import csv
import api.models

class Command(BaseCommand):
  help = 'Retrieve all messages for a given OpenAI thread and write only the text content to messages.csv'

  def handle(self, *args, **kwargs):

    try:
      assistant = api.models.OpenAIAssistant.objects.filter(model="gpt-4o-mini").first()
      name = "General Knowledge Assistant - 4o Mini"
      instructions = assistant.instructions
      assistant_id = assistant.assistant_id
      openai.beta.assistants.update(
      assistant_id=assistant_id,
      instructions=instructions,
      name=name,
      tools=[{'type': 'file_search'}],
    )
      print(f"Assistant {assistant_id} updated successfully.")
    except Exception as e:
      print(f"Error updating assistant: {e}")
      return
      
