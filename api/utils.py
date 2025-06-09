from django.contrib.auth.models import User
# from langchain_openai import ChatOpenAI
from api.models import User, Conversation, OpenAIAssistant, OpenAIThread,User
from api.serializers import OpenAIThreadSerializer
from django.core.exceptions import ObjectDoesNotExist
import openai, time


def get_user_threads(user_id):
  try:
    # Fetch all conversations for the given user ID
    conversations = Conversation.objects.filter(user_id=user_id)
    
    # Serialize the conversations
    serializer = OpenAIThreadSerializer(conversations, many=True)
    
    # Return the serialized data as a JSON response
    return {"status": "success", "data": serializer.data}
  except Exception as e:
    return {"status": "failure", "error": str(e)}
  

def get_latest_gpt_response(run, thread_id, print_all_messages: bool = False):
  # wait for completion
  client = openai.OpenAI()

  while True:
    run = client.beta.threads.runs.retrieve(
      thread_id=thread_id,
      run_id=run.id
    )
    if run.status == "completed":
      try:
        usage = run.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        print(f"Run completed with {input_tokens} input tokens, {output_tokens} output tokens, total {total_tokens} tokens.")
        print_costs_for_all_models(input_tokens, output_tokens)
        break
      except Exception as e:
        print(f"Error retrieving usage information: {e}")
        raise Exception("Run completed but usage information is missing or malformed.")
    elif run.status in ["failed", "cancelled", "expired"]:
      raise Exception(f"Run ended with status: {run.status}")
    time.sleep(0.5)

  # fetch messages
  messages = client.beta.threads.messages.list(thread_id=thread_id)
  message_data = messages.data

  if print_all_messages:
    print("All messages in the thread:")
    for msg in message_data:
      if msg.role == "user":
        print("User input:", msg.content)
      elif msg.role == "assistant":
        for block in msg.content:
          if block.type == "text":
            print("Assistant response:", block.text.value)

  for msg in message_data:          
    if msg.role == "assistant":
      for block in msg.content:      
        if block.type == "text":
          print("Assistant response:", block.text.value)
          return block.text.value
  return None

def get_user_thread_list(user_id: int,sort_by_last_accessed:bool=False):
  try:
    user = User.objects.get(id=user_id)
  except ObjectDoesNotExist:
    return []

  threads = OpenAIThread.objects.filter(user=user).order_by('-created_at')
  if sort_by_last_accessed:
    threads = threads.order_by('-last_accessed')
  return [
    {"name": thread.name, "thread_id": thread.thread_id}
    for thread in threads
  ]


def rename_thread(user_id: int, thread_id: str, new_name: str):
  try:
    thread = OpenAIThread.objects.get(user_id=user_id, thread_id=thread_id)
    thread.name = new_name
    thread.save()
    print(f"Thread {thread_id} renamed to {new_name}")
  except OpenAIThread.DoesNotExist:
    print(f"Thread {thread_id} not found for user {user_id}")
    raise ValueError("Thread not found")
  except Exception as e:
    print(f"Error renaming thread: {e}")
    raise

def delete_thread(user_id: int, thread_id: str):
  try:
    thread = OpenAIThread.objects.get(user_id=user_id, thread_id=thread_id)
    thread_name = thread.name
    thread.delete()
    print(f"Thread - {thread_name}, id - {thread_id} deleted for user {user_id}")
    return thread_name
  except OpenAIThread.DoesNotExist:
    print(f"Thread {thread_id} not found for user {user_id}")
    raise ValueError("Thread not found")
  except Exception as e:
    print(f"Error deleting thread: {e}")
    raise

def calculate_gpt_cost(model: str, input_tokens: int, output_tokens: int) -> float:
  pricing = {
    "gpt-4o": {
      "input": 0.0025,
      "output": 0.01
    },
    "gpt-4o-mini": {
      "input": 0.00015,
      "output": 0.0006
    },
    "gpt-4.1": {
      "input": 0.01,
      "output": 0.03
    },
    "gpt-4.1-mini": {
      "input": 0.0015,
      "output": 0.002
    }
  }

  if model not in pricing:
    raise ValueError(f"Unknown model: {model}")

  rate = pricing[model]
  cost = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1000
  print(round(cost, 6))

def print_costs_for_all_models(input_tokens: int, output_tokens: int):
  pricing = {
    "gpt-4o": {
      "input": 0.0025,
      "output": 0.01
    },
    "gpt-4o-mini": {
      "input": 0.00015,
      "output": 0.0006
    },
    "gpt-4.1": {
      "input": 0.01,
      "output": 0.03
    },
    "gpt-4.1-mini": {
      "input": 0.0015,
      "output": 0.002
    }
  }

  for model, rate in pricing.items():
    cost = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1000
    print(f"{model}: ${round(cost, 6)}")

