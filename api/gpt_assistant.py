import openai, time, os
from api.models import OpenAIThread, User, UserFile
from django.core.exceptions import ObjectDoesNotExist
from api import utils, models
from django.conf import settings
from PIL import Image
import io


def run_assistant(user_id, thread_id, user_input, files=[], documents=[], assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7", max_prompt_tokens=20000):
  print("Starting run_assistant routine...")
  print("thread_id", thread_id)

  if thread_id is None:
    print("Thread not found, creating new thread...")
    utils.create_new_thread_for_user(user_id)
  print("User Input:", user_input)
  print("Documents Provided:", len(documents))
  if documents:
    [print("Document:", doc.name) for doc in documents]
  
  print("Files Provided:", len(files))
  if files:
    [print(f"File Provided: {f.name}") for f in files]

  print("")
  attachments = prepare_openai_attachments(documents)
  content = prepare_openai_content(user_input, files)

  kwargs = {}
  if attachments:
    print("Attachments: ", attachments)
    kwargs["attachments"] = attachments

  print("Creating OpenAI message...")
  try:
    openai.beta.threads.messages.create(
      thread_id=thread_id,
      role="user",
      content=content,
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
      "assistants": [".pdf", ".txt", ".csv", ".docx"],
      "vision": [".png", ".jpg", ".jpeg", ".webp"]
    }
    
    if filename.lower().endswith(tuple(file_types_by_purpose["vision"])):
      return "vision"
    elif filename.lower().endswith(tuple(file_types_by_purpose["assistant"])):
      return "assistants"
    else:
      raise ValueError(f"Unsupported file type for filename: {filename}. Supported types are: {file_types_by_purpose['assistant'] + file_types_by_purpose['vision']}")



def prepare_openai_content(user_input, img_files):
  """Prepare OpenAI content files such as user input and images"""
  print("Preparing OpenAI content...")
  content = []
  print("Adding user input to content...")
  content.append({
    "type": "text",
    "text": user_input
  })
  for img_file in img_files:
    print("Creating OpenAI image file for filename:", img_file.name, "...")
    try:
      openai_img = openai.files.create(
      file=(img_file.name, img_file.read()),
      purpose="assistants"
      )
    except Exception as e:
      print("Error creating OpenAI image file:", e)
      raise ValueError(f"Error creating OpenAI image file: {e}. Please check your input and try again.")
    print("OpenAI image file created with ID:", openai_img.id)
    content.append({
      {
      "type": "image_file",
      "image_file": {
        "file_id": openai_img.id
        }
      }
    })
  print("OpenAI content prepared:", content)    
  return content


def prepare_openai_attachments(documents):
  print("Preparing OpenAI attachments...")
  attachments = []

  # All cases
  # # Create File (if applicable)
  for f in documents:
    print("Processing OpenAI document file for filename:", f.name, "...")

    try:
      print("Creating OpenAI document file for:", f.name)
      openai_file = openai.files.create(
      file=(f.name, f.read()),
      purpose="assistants"
      )
    except Exception as e:
      print("Error creating OpenAI file:", e)
      raise ValueError(f"Error creating OpenAI file: {e}. Please check your input and try again.")

    print("Creating Attachment for file:", f.name)
    new_attachment = {
      "file_id": openai_file.id,
      "tools": [{"type": "file_search"}],
    }
    attachments.append(new_attachment)
    print("Attachments so far:", attachments)
  return attachments

