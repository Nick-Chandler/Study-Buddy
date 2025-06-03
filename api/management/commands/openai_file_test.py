from django.core.management.base import BaseCommand, CommandError
import api.models as models
import openai,time,os

class Command(BaseCommand):
  help = "Testing openai file handling"

  def handle(self, *args, **options):
    try:
      openai.api_key = os.getenv("OPENAI_API_KEY")

      # Get Assistant
      assistant = models.OpenAIAssistant.objects.all().first()
      print(assistant)
      print(f"Using Assistant: {assistant.name} ({assistant.assistant_id})")
      
      
      openai_file = openai.files.create(
        file=open("api/1042_Final_Review  (2).pdf", "rb"),
        purpose="assistants"
      )
      # Create Thread and attach OpenAI File
      thread_id = "thread_h6r2VaxsBKNCJr8dZGJc7Ivg"
      # print(f"Thread created with ID: {thread.id}")
      # # Create a Run
      openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content="Summarize the attached document.",
        attachments=[{
          "file_id": openai_file.id,
          "tools": [{"type": "file_search"}]
        }]
      )

      run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant.assistant_id,
        max_prompt_tokens=20000
      )
      print(f"Run created with ID: {run.id}")
      # # Poll for Response
      while True:
        run_status = openai.beta.threads.runs.retrieve(
          thread_id=thread_id,
          run_id=run.id
        )
        if run_status.status == "completed":
          break
        time.sleep(1)
      # # Print Content
      messages = openai.beta.threads.messages.list(thread_id=thread_id)
      for msg in messages.data:
        print(msg.role)               # "user" or "assistant"
        print(msg.content[0].text.value)  # The actual message text
    except Exception as e:
      raise CommandError(f"An error occurred: {e}")
