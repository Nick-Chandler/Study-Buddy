import openai, time, os
from api.models import OpenAIThread, User, UserFile
from django.core.exceptions import ObjectDoesNotExist
from api import utils, models
from django.conf import settings
from PIL import Image
import io


def run_assistant(user_id, thread_id, user_input, files, assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7", max_prompt_tokens=20000):
  print("Starting run_assistant...")
  print("thread_id", thread_id)

  if thread_id is None:
    print("Thread not found, creating new thread...")
    utils.create_new_thread_for_user(user_id)
  print("User Input:", user_input) 
  [print(f"File Provided: {f.name}") for f in files]
  attachments = []

  # All cases
  # # Create File (if applicable)
  for i, f in enumerate(files):
    if f.name:
      file_purpose = find_file_purpose(f.name)
      print("Retrieving file for user:", user_id, "with filename:", f.name, "...")
      print("Creating OpenAI file for filename:", f.name, "...")

      try:
        # Load image using Pillow
        img = Image.open(f)

        # Save to in-memory buffer
        buffer = io.BytesIO()
        img_format = img.format if img.format else "PNG"
        img.save(buffer, format=img_format)
        buffer.name = f.name
        buffer.seek(0)

        openai_file = openai.files.create(
          file=buffer,
          purpose="vision"  # or "assistants" depending on your use case
        )
      except Exception as e:
        print("Error creating OpenAI file:", e)
        raise ValueError(f"Error creating OpenAI file: {e}. Please check your input and try again.")

      print("Creating Attachments...")
      new_attachment = {
        "file_id": openai_file.id,
        "tools": [{"type": "file_search"}],
      }
      if file_purpose == "assistants":
        print("File purpose is for assistants.")
        new_attachment["tools"] = [{"type": "file_search"}]
      attachments.append(new_attachment)
      print("Attachments so far:", attachments)

  kwargs = {}
  if attachments:
    print("Attachments: ", attachments)
    kwargs["attachments"] = attachments
  print("Creating OpenAI message...")
  try:
    openai.beta.threads.messages.create(
      thread_id=thread_id,
      role="user",
      content=user_input,
      **kwargs
    )
  except Exception as e:
    print("InvalidRequestError:", e)
    raise ValueError(f"Invalid request: {e}. Please check your input and try again.")


  print("Creating OpenAI run...")
  try:
    run = openai.beta.threads.runs.create(
      thread_id=thread_id,
      assistant_id=assistant_id,
      max_prompt_tokens=max_prompt_tokens
    )
  except Exception as e:
    print("InvalidRequestError:", e)
    raise ValueError(f"Invalid request: {e}. Please check your input and try again.")
  print("Retrieving response...")
  response = utils.get_latest_gpt_response(run, thread_id)
  print("Response received:", response)
  return response

def find_file_purpose(filename):
    print("Finding file purpose for:", filename)
    file_types_by_purpose = {
      "assistant": [".pdf", ".txt", ".csv", ".docx"],
      "vision": [".png", ".jpg", ".jpeg", ".webp"]
    }
    
    if filename.lower().endswith(tuple(file_types_by_purpose["vision"])):
      return "vision"
    elif filename.lower().endswith(tuple(file_types_by_purpose["assistant"])):
      return "assistants"
    else:
      raise ValueError(f"Unsupported file type for filename: {filename}. Supported types are: {file_types_by_purpose['assistant'] + file_types_by_purpose['vision']}")
