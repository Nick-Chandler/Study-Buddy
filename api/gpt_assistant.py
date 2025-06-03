import openai, time, os
from api.models import OpenAIThread, User, UserFile
from django.core.exceptions import ObjectDoesNotExist
from api import utils, models
from django.conf import settings


def run_assistant(user_id, thread_id, user_input, filename="", assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7", max_prompt_tokens=20000):
  print("Starting run_assistant...")
  # create file (Postponed)
  # get or create thread
  print("Fetching Thread ID...")
  print("thread_id", thread_id)
  
  if thread_id is None:
    print("Thread not found, creating new thread...")
    utils.create_new_thread_for_user(user_id)
  
  file_purpose = find_file_purpose(filename)

  # All cases
  # # Create File (if applicable)
  if file_purpose:
    file = UserFile.objects.get(user_id=user_id, filename=filename).file.open("rb")
    openai_file = openai.files.create(
      file=file,
      purpose=file_purpose
    )
    attachments = [{
      "file_id": openai_file.id,
      "tools": []
      }]
    if file_purpose == "assistants":
      attachments[0]["tools"].append({"type": "file_search"})

  kwargs = {}
  if attachments:
    kwargs["attachments"] = attachments
  openai.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=user_input,
    **kwargs
  )


  print("OpenAI message created successfully.")
  # poll until response
  print("Creating run...")
  run = openai.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    max_prompt_tokens=max_prompt_tokens
  )
  print("Retrieving response...")
  response = utils.get_latest_gpt_response(run, thread_id)
  print("Response received:", response)
  return response

def find_file_purpose(filename):
    """
    Determine the purpose of the file based on its extension.
    """
    file_types_by_purpose = {
      "assistant": [".pdf", ".txt", ".csv", ".docx"],
      "vision": [".png", ".jpg", ".jpeg", ".webp"]
    }
    
    if filename.lower().endswith(tuple(file_types_by_purpose["vision"])):
      return "vision"
    elif filename.lower().endswith(tuple(file_types_by_purpose["assistant"])):
      return "assistants"
    else:
      return None
