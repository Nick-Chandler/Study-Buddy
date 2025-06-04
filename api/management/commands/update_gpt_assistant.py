from django.core.management.base import BaseCommand
import openai
import csv
import api.models

class Command(BaseCommand):
  help = 'Retrieve all messages for a given OpenAI thread and write only the text content to messages.csv'

  def handle(self, *args, **kwargs):

    try:
      assistant_id = api.models.OpenAIAssistant.objects.all().first().assistant_id
      openai.beta.assistants.update(
      assistant_id=assistant_id,
      instructions="You are a general chatbot specializing in homework and study assistance. Be concise and clear in your responses. If you don't know the answer, say 'I don't know'.",
      name="Homework Assistant",
      tools=[{'type': 'file_search'}, {'type': 'code_interpreter'}],
    )
      print(f"Assistant {assistant_id} updated successfully.")
    except Exception as e:
      print(f"Error updating assistant: {e}")
      return
      
