import openai, time, os
from api.models import OpenAIAssistant, OpenAIThread, User, UserFile
from django.core.exceptions import ObjectDoesNotExist
from api import utils, models
from django.conf import settings
from PIL import Image
import io


def run_assistant(user_id, thread_id, user_input, user_file=None, assistant_id = "asst_S1LowFqv8XSbWhmYzDggiD8g", max_prompt_tokens=20000):

  print("Starting run_assistant routine...")
  assistant = OpenAIAssistant.objects.get(assistant_id=assistant_id)
  print("Using Assistant:", assistant.name, "with ID:", assistant.assistant_id, "and model:", assistant.model)
  print("thread_id", thread_id)

  print("User Input:", user_input)
  print("Document Provided:", user_file.filename if user_file else "No document provided")
  if user_file:
    print(user_file.filename)

  content = prepare_openai_content(user_input, user_file)


  print("Creating OpenAI message...")
  print("Thread ID:", thread_id)
  print("Role: user")
  print("Content:", content)
  try:
    response = openai.beta.threads.messages.create(
      thread_id=thread_id,
      role="user",
      content=content,
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



def prepare_openai_content(user_input,user_file=None):
  """Prepare OpenAI content files such as user input and images"""
  print("Preparing OpenAI content...")
  print("Adding user input to content...")
  context = ""
  if user_file:
    context = user_file.extract_text()
  content=f""" Answer the following question to the best of your ability. 
  If needed use the context provided below (if available) if it will help you better answer the question:
  {user_input}

  ---context---
  {context}
  """
  
  
  # print("OpenAI content prepared:", content)    
  return content
