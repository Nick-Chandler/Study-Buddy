import openai, time
from api.models import OpenAIThread, User
from django.core.exceptions import ObjectDoesNotExist
from api import utils


def run_assistant(user_id, thread_idx, user_input):
  print(f"Assistant function called with user_id: {user_id}, thread_idx: {thread_idx}, user_input: {user_input}")
  assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7"
  # create file (Postponed)
  # get or create thread
  print("Fetching Thread ID...")
  thread_id = utils.get_nth_thread_id(user_id, thread_idx)
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
  assistant_id=assistant_id
)
  print("Retrieving response...")
  response = utils.get_latest_gpt_response(run, thread_id)
  print("Response received:", response)
  return response

