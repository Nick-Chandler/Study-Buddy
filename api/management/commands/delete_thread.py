from django.core.management.base import BaseCommand
from api.models import OpenAIAssistant, OpenAIThread
import openai
import os

class Command(BaseCommand):
  help = "Create and store a single OpenAI Assistant"

  def add_arguments(self, parser):
    parser.add_argument('thread_id', type=str, help='The ID of the OpenAI thread')

  def handle(self, *args, **kwargs):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    thread_id = kwargs['thread_id']

    try:
      thread = OpenAIThread.objects.get(thread_id=thread_id).delete()
      print(f"Thread {thread_id} deleted successfully from models.")
      openai.beta.threads.delete(thread_id=thread_id)
      print(f"Thread {thread_id} deleted successfully from openai.")
    
    except Exception as e:
      print(f"Error deleting thread: {e}")
      return
      
