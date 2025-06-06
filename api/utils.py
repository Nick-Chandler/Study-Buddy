from django.contrib.auth.models import User
# from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from api.models import User, Conversation, OpenAIAssistant
from api.models import OpenAIThread, User
from api.serializers import OpenAIThreadSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import openai, time

client = openai.OpenAI()


class History:

  def __init__(self):
    self.messages = []

  def append(self, message):
    self.messages.append(message)
  def add_messages(self, messages: list):
      """Add a list of messages to the store"""
      self.messages.extend(messages)
  
  def __str__(self):
    return f"History({self.messages})"


def init_memory(cid):
  print("Retrieving conversation...")
  try:
    c = Conversation.objects.get(conversation_id=cid)
  except Conversation.DoesNotExist:
    print("No conversation found with the given ID.")
    print("Creating new conversation...")
    h = History()
    print(h)
    return h

  print("ordering messages by timestamp...")
  messages = c.messages.order_by("timestamp")

  h = History()

  for msg in messages:
    if msg.role == "human":
      h.append(HumanMessage(content=msg.content))
    elif msg.role == "ai":
      h.append(AIMessage(content=msg.content))
  return h


def form_prompt(user_input, history):
  
  prompt_template = ChatPromptTemplate.from_messages(
      [
          SystemMessage(
            content="You are a homework assistant."
          ),
          MessagesPlaceholder(variable_name="messages"),
            ("human", "{user_input}"),
      ]
  )

  return prompt_template

  
def form_chain(prompt_template, model, history, user_input):
  prompt_template.invoke({
    "messages": history,
    "user_input": user_input,
  })
  return form_chain

def build_runnable(chain):
  try:
    chain_with_memory = RunnableWithMessageHistory(
    chain,
    init_memory,
    input_messages_key="user_input",
    history_messages_key="messages",
    )
  except Exception as e:
    print(f"Error building runnable: {e}")
    raise
  return chain_with_memory


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

def user_id_by_cid(cid):
  print(f"Fetching user ID for conversation ID: {cid}")
  try:
    # Fetch the conversation by its ID
    conversation = Conversation.objects.get(conversation_id=cid)
    
    # Return the user ID associated with the conversation
    print(f"Got User ID: {conversation.user.id}")
    return conversation.user.id
  except Conversation.DoesNotExist:
    return None

def get_last_user_conversation(user_id):
  try:
    # Fetch the last conversation for the given user ID, ordered by last_accessed
    conversation = Conversation.objects.filter(user_id=user_id).order_by('-last_accessed').first()
    print(f"Got last conversation: {conversation}")
    
    if conversation:
      # Serialize the conversation
      last_accessed_conversation = conversation.conversation_id
      print(f"Last accessed conversation ID: {last_accessed_conversation}")
      
      # Return the serialized data as a JSON response
      return last_accessed_conversation
    else:
      return None
  except Exception as e:
    return {"status": "failure", "error": str(e)}
  
def get_or_create_user_thread(user_id,thread_idx):
  thread_id = get_nth_thread_id(user_id, thread_idx)
  if thread_id is None:
    thread_id = create_new_thread_for_user(user_id)
  

def get_nth_thread_id(user_id: int, n: int):
  try:
    user = User.objects.get(id=user_id)
  except User.DoesNotExist:
    return None

  threads = OpenAIThread.objects.filter(user=user).order_by('-created_at')
  if n < 0 or n >= threads.count():
    return None

  return threads[n].thread_id

def create_new_thread_for_user(user_id: int, name: str):
  try:
    user = User.objects.get(id=user_id)
  except User.DoesNotExist:
    return None

  thread = openai.beta.threads.create()  # Create via OpenAI API

  new_thread = OpenAIThread.objects.create(
    user=user,
    name=name,
    thread_id=thread.id,
    created_at=timezone.now(),
    last_accessed=timezone.now()
  )

  return new_thread.thread_id

def get_latest_gpt_response(run, thread_id):
  # wait for completion
  while True:
    run = openai.beta.threads.runs.retrieve(
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
  messages = openai.beta.threads.messages.list(thread_id=thread_id)

  for msg in messages.data:          # newest first
    if msg.role == "assistant":
      for block in msg.content:      # look for text blocks only
        if block.type == "text":
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

def thread_idx_to_thread_id(user_id: int, thread_idx: int):
  try:
    user = User.objects.get(id=user_id)
  except ObjectDoesNotExist:
    return None

  threads = OpenAIThread.objects.filter(user=user).order_by('-created_at')
  if thread_idx < 0 or thread_idx >= threads.count():
    return None

  return threads[thread_idx].thread_id

def fetch_thread_messages(thread_id: str):
  print(f"Fetching messages for thread ID: {thread_id}")
  msgs = []

  page = client.beta.threads.messages.list(
    thread_id=thread_id,
    limit=100,
  )
  print(f"Got page Response")
  while page.data:
    for m in page.data:
      if m.role == "user":
        msgs.append({
          'id': m.id,
          'role': "human",
          'text': m.content[0].text.value
        })
      elif m.role == "assistant":
        msgs.append({
          'id': m.id,
          'role': "ai",
          'text': m.content[0].text.value
        })

    if not page.has_next_page:
      break
    else :
      page = page.get_next_page()

  return msgs

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

