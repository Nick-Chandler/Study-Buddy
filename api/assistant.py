import openai, time
from api.models import OpenAIThread, User
from django.core.exceptions import ObjectDoesNotExist
import api.utils


def assistant(user_id, thread_idx, user_input):
  assistant_id = "asst_ceOd9c6y55I9vToqnkJKUnj7"
  # create file (Postponed)
  # get or create thread
  thread_id = api.utils.get_nth_thread_id(user_id, thread_idx)
  if thread_id is None:
    api.utils.create_new_thread_for_user(user_id)
  # run assistant
  openai.beta.threads.messages.create(
  thread_id=thread_id,
  role="user",
  content=user_input,
  # file_ids=[image_file.id]
)
  # poll until response
  run = openai.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant.id
)
  response = api.utils.get_latest_gpt_response(run, thread_id)
  return response

