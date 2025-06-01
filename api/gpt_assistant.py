import openai, time, os
from api.models import OpenAIThread, User, UserFile
from django.core.exceptions import ObjectDoesNotExist
from api import utils
from django.conf import settings


def run_assistant(user_id, thread_id, user_input, filename=None):
  print(f"Assistant function called with user_id: {user_id}, thread_id: {thread_id}, user_input: {user_input}")
  assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7"
  # create file (Postponed)
  # get or create thread
  print("Fetching Thread ID...")
  print("thread_id", thread_id)
  if thread_id is None:
    print("Thread not found, creating new thread...")
    utils.create_new_thread_for_user(user_id)
  # run assistant
  print("Creating Message...")
  print("Current User Input:", user_input)
  openai.beta.threads.messages.create(
  thread_id=thread_id,
  role="user",
  content=user_input,
  # file_ids=[image_file.id]
)
  # poll until response
  print("Creating run...")
  run = openai.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id,
  max_prompt_tokens=20000
)
  print("Retrieving response...")
  response = utils.get_latest_gpt_response(run, thread_id)
  print("Response received:", response)
  return response

# def prepare_file(user_id, filename):
#   try:
#     # Query the UserFile model for the file
#     user_file = UserFile.objects.get(filename=filename, user_id=user_id)
    
#     # Construct the full file path
#     file_path = os.path.join(settings.MEDIA_ROOT, user_file.file.name)
    
#     # Open and return the file
#     with open(file_path, 'rb') as f:
#         file_data = f.read()
#     return file_data
#   except UserFile.DoesNotExist:
#       print(f"File with filename '{filename}' not found for user ID {user_id}.")
#       return None
#   except Exception as e:
#       print(f"An error occurred while accessing the file: {e}")
#       return None
