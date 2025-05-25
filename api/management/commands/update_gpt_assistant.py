from django.core.management.base import BaseCommand
import openai
import csv

class Command(BaseCommand):
  help = 'Retrieve all messages for a given OpenAI thread and write only the text content to messages.csv'

  def add_arguments(self, parser):
    parser.add_argument('assistant_id', type=str, help='The ID of the OpenAI Assistant')

  def handle(self, *args, **kwargs):
    assistant_id = kwargs['assistant_id']

    try:
      openai.beta.assistants.update(
      assistant_id=assistant_id,
      instructions="You are a general chatbot specializing in homework and study assistance. Be concise and clear in your responses. If you don't know the answer, say 'I don't know'.",
      name="Homework Assistant",
    )
      print(f"Assistant {assistant_id} updated successfully.")
    except Exception as e:
      print(f"Error updating assistant: {e}")
      return
      
