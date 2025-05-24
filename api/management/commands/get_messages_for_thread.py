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
      all_messages = []
      messages = openai.beta.threads.messages.list(thread_id=thread_id)

      all_messages.extend(messages.data)

      if hasattr(messages, 'auto_paging_iter'):
        for message in messages.auto_paging_iter():
          all_messages.append(message)

      with open('messages.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Content'])
        
        for message in all_messages:
          writer.writerow([message.content])

      print('Messages written to messages.csv')

    except Exception as e:
      print(f"Error retrieving messages: {e}")
