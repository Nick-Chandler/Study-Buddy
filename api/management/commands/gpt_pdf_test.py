from django.core.management.base import BaseCommand
from api.models import OpenAIAssistant
from api.utils import print_costs_for_all_models
import openai, time


class Command(BaseCommand):
  help = "Send a prompt and PDF to the GPT Assistant API"

  def handle(self, *args, **options):
    prompt = "List every problem in this pdf" 
    pdf_path = "api/Math Concepts Practice Exam 1.pdf"

    # Upload the file
    with open(pdf_path, "rb") as f:
      uploaded_file = openai.files.create(file=(pdf_path, f), purpose="assistants")

    # Create assistant
    assistant = OpenAIAssistant.objects.filter(model="gpt-4.1-mini").first()

    # Create thread
    thread = openai.beta.threads.create()

    # Attach message with file
    openai.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=prompt,
      attachments=[{"file_id": uploaded_file.id, "tools": [{"type": "file_search"}]}]
    )

    # Run
    run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.assistant_id)

    # Wait for completion
    while True:
      run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
      if run.status == "completed":
        usage = run.usage
        print(f"Input tokens: {usage.prompt_tokens}")
        print(f"Output tokens: {usage.completion_tokens}")
        print(f"Total tokens: {usage.total_tokens}")
        print_costs_for_all_models(usage.prompt_tokens, usage.completion_tokens)
        break
      time.sleep(1)

    # Get messages
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
      if msg.role == "assistant":
        print("Assistant: ", msg.content[0].text.value)
