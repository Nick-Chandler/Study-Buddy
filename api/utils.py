from django.contrib.auth.models import User
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from api.models import User, Conversation, Message

def init_llm(model="gpt-4o-mini", model_provider="openai"):
  return ChatOpenAI(model_name="gpt-4o-mini")

def init_memory(cid):
  print("Retrieving conversation...")
  try:
    c = Conversation.objects.get(conversation_id=cid)
  except Conversation.DoesNotExist:
    return []

  print("ordering messages by timestamp...")
  messages = c.messages.order_by("timestamp")
  h = []

  class History:

    def __init__(self):
      self.messages = []

    def append(self, message):
      self.messages.append(message)
    def add_messages(self, messages: list):
        """Add a list of messages to the store"""
        self.messages.extend(messages)
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
    convo = Conversation.objects.get(conversation_id=cid)
    print(convo.id)
    Message.objects.create(
        conversation=convo,
        role="human",
        content=human_msg
    )

    Message.objects.create(
        conversation=convo,
        role="ai",
        content=ai_msg
    )

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
    response = runnable.invoke(
      {"user_input": user_input},
      config={"configurable": {"session_id": cid}}
    ).content
  except Exception as e:
    print(f"Error running chain: {e}")
    raise
  # store messages
  print("Storing messages...")
  store_message(user_input, response, cid)
  return response
    

