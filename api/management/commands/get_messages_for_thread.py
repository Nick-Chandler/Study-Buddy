from django.core.management.base import BaseCommand
import openai
import csv

class Command(BaseCommand):
  help = 'Retrieve all messages for a given OpenAI thread and write only the text content to messages.csv'

  def add_arguments(self, parser):
    parser.add_argument('thread_id', type=str, help='The ID of the OpenAI thread')

  def handle(self, *args, **kwargs):
    thread_id = kwargs['thread_id']

    try:
      response = openai.beta.threads.messages.list(thread_id=thread_id)
      for i,msg in enumerate(response.data):
        print(f"Message {i+1}:")
        print("----------------------------------")
        print(f"Message Id: {msg.id}")
        print(f"Message Role: {msg.role}")
        print(f"Message Content: {msg.content}")
    except Exception as e:
      print(f"Error retrieving messages: {e}")
      return
      
