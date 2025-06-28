import openai, time, os
from api.models import OpenAIAssistant, OpenAIThread, User, UserFile
from django.core.exceptions import ObjectDoesNotExist
from api import utils, models
from django.conf import settings
from PIL import Image
import io


def run_assistant(user_id, thread_id, user_input, files=[], user_file=None, assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7", max_prompt_tokens=20000):

  print("Starting run_assistant routine...")
  assistant = OpenAIAssistant.objects.get(assistant_id=assistant_id)
  print("Using Assistant:", assistant.name, "with ID:", assistant.assistant_id, "and model:", assistant.model)
  print("thread_id", thread_id)

  if thread_id is None:
    print("Thread not found, creating new thread...")
    utils.create_new_thread_for_user(user_id)
  print("User Input:", user_input)
  print("Document Provided:", user_file.filename if user_file else "No document provided")
  if user_file:
    print(user_file.filename)

  if files:
    print("Files Provided:", len(files))
    [print(f"File Provided: {f.name}") for f in files]

  content = prepare_openai_content(user_input, files)
  if user_file:
    kwargs = prepare_openai_attachments(user_file)


  print("Creating OpenAI message...")
  print("Thread ID:", thread_id)
  print("Role: user")
  if content:
    print("Content:", content)
  print("Attachment:", kwargs['attachments'] if 'attachments' in kwargs else "No attachments")
  try:
    response = openai.beta.threads.messages.create(
      thread_id=thread_id,
      role="user",
      content=content,
      **kwargs
    )

    if response.attachments and len(response.attachments) > 0:
      print("Document successfully attached!")
      for attachment in response.attachments:
        print("Attachment:", attachment)
    else:
      print("No document found in message.")
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
  response = utils.get_latest_gpt_response(run, thread_id, print_all_messages=False)
  # print("Response received:", response)
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
  # print("OpenAI content prepared:", content)    
  return content


def prepare_openai_attachments(user_file):
  print("Preparing OpenAI attachments...")
  kwargs = {}

  # Create File (if applicable)
  print("Processing OpenAI document file for filename:", user_file.filename, "...")
  try:
    print("Creating OpenAI document file for:", user_file.filename)
    openai_file = openai.files.create(
      file=(user_file.filename, user_file.file.read()),
      purpose="assistants"
    )
  except Exception as e:
    print("Error creating OpenAI file:", e)
    raise ValueError(f"Error creating OpenAI file: {e}. Please check your input and try again.")
  wait_for_file_processed(openai_file.id)
  print("Creating Attachment for file:", user_file.filename)
  new_attachment = {
    "file_id": openai_file.id,
    "tools": [{"type": "file_search"}],
  }
  print("Attachment: ", new_attachment)
  kwargs["attachments"] = [new_attachment]
  return kwargs

def wait_for_file_processed(file_id, timeout=30, poll_interval=.5):
  """
  Polls the OpenAI API until the file with file_id is processed or timeout is reached.
  Returns True if processed, raises an Exception otherwise.
  """
  start_time = time.time()
  while True:
    file_status = openai.files.retrieve(file_id)
    status = getattr(file_status, "status", None) or file_status.get("status")
    print(f"Polling file {file_id}: status={status}")
    if status == "processed":
      print(f"File {file_id} is processed and ready.")
      end_time = time.time()
      print(f"File {file_id} processed in {end_time - start_time:.2f} seconds.")
      return True
    if status == "failed":
      raise Exception(f"File {file_id} processing failed.")
    if time.time() - start_time > timeout:
      raise TimeoutError(f"Timeout: File {file_id} was not processed within {timeout} seconds.")
    time.sleep(poll_interval)