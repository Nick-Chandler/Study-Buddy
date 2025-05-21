from django.contrib.auth.models import User
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from api.models import User, Conversation, Message
from .serializers import ConversationSerializer

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

def init_llm(model="gpt-4o-mini", model_provider="openai"):
  return ChatOpenAI(model_name="gpt-4o-mini")

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


def store_message(human_msg, ai_msg, cid):
    print(f"Storing messages for conversation ID: {cid}")
    convo = Conversation.objects.get(conversation_id=cid)
    print(f"Got conversation: {convo}")
    Message.objects.create(
        conversation=convo,
        role="human",
        content=human_msg
    )
    print(f"Created message for user: {human_msg}")

    Message.objects.create(
        conversation=convo,
        role="ai",
        content=ai_msg
    )
    print(f"Created message for AI: {ai_msg}")

    print("Messages stored successfully")
  
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

def update_conversation(uid,cid,user_input):
  # load history
  print("Loading history...")
  history = init_memory(cid)
  # prompt template
  print("Forming prompt...")
  prompt = form_prompt(user_input, history)
  # build llm
  print("Initializing LLM...")
  llm = init_llm()
  # build chain
  print("Building chain...")
  chain = prompt | llm
  # infuse memory
  print("Infusing memory...")
  runnable = build_runnable(chain)
  # run chain
  print("Running chain...")
  try:
    print(f"User input: {user_input}")
    print(f"cid: {cid}")
    response = runnable.invoke(
      {"user_input": user_input},
      config={"configurable": {"session_id": cid}}
    ).content
  except Exception as e:
    print(f"Error running chain: {e}")
    raise
  # store messages
  print("Storing messages...")
  print(f"User input: {user_input}")
  print(f"Response: {response}")
  print(f"cid: {cid}")
  store_message(user_input, response, cid)
  return response


def get_user_conversations(user_id):
  try:
    # Fetch all conversations for the given user ID
    conversations = Conversation.objects.filter(user_id=user_id)
    
    # Serialize the conversations
    serializer = ConversationSerializer(conversations, many=True)
    
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
