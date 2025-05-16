from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from api.models import User, Conversation, Message

def init_llm(model="gpt-4o-mini", model_provider="openai"):
  return ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def init_memory(user_id, cid=None):
  print("Initializing memory...")
  user = User.objects.get(id=user_id)
  conversation = Conversation.objects.filter(user=user).first()
  if not conversation:
    conversation = Conversation.objects.create(user=user, name="Default Conversation")
  for message in conversation.messages.all():
    if message.role == "human":
      print(f"User: {message.content}")
    else:
      print(f"AI: {message.content}")

  return ConversationBufferMemory()

def init_conversation():
  return ConversationChain(
    llm=init_llm(),
    memory=init_memory(),
    verbose=True  # optional: prints the chain's reasoning
  )