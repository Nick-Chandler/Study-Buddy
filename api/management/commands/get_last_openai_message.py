from django.core.management.base import BaseCommand
import openai
import csv
import api.models

class Command(BaseCommand):
  help = 'Retrieve all messages for a given OpenAI thread and write only the text content to messages.csv'

  def handle(self, *args, **kwargs):

    try:
      thread_id = "thread_QQYIkzXyHiTZJ1OJqAfHc0Fo"
      messages = openai.beta.threads.messages.list(thread_id=thread_id)
      for msg in messages.data:
        print("Message:", msg)
        print(f"Message ID: {msg.id}, Role: {msg.role}, Created At: {msg.created_at}")
        if msg.role == "user":
          print("Latest user message:")
          for block in msg.content:
            print("Block:", block)
            if block.type == "text":
              print(block.text.value)
            elif block.type == "image_file":
              print(f"[Image file ID: {block.image_file.file_id}]")
          break  # Only want the most recent user message
    except Exception as e:
      print(f"Error printing message: {e}")
      return
      
