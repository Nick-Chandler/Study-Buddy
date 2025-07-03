from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
import openai,uuid, numpy as np, os
from PyPDF2 import PdfReader

class Conversation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
  name = models.CharField(max_length=255)  # Name of the conversation
  conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique ID
  last_accessed = models.DateTimeField(auto_now=True)  # Automatically updates to the current timestamp on save

  def __str__(self):
    return self.name
  
from django.db import models

class OpenAIAssistant(models.Model):
  assistant_id = models.CharField(max_length=100, unique=True)
  name = models.CharField(max_length=100)
  instructions = models.TextField()
  model = models.CharField(max_length=50, default="gpt-4o")
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} ({self.assistant_id})"
  
def generate_thread():
  # Call OpenAI API
  thread = openai.beta.threads.create()

  print(f"New OpenAIThread created: {thread.id}")
  return thread.id
  
class OpenAIThread(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='openai_threads')
  name = models.CharField(max_length=255)
  thread_id = models.CharField(max_length=100, unique=True, default=generate_thread, primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_accessed = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Thread for {self.user.username}: {self.thread_id}"
  
  def rename_thread(self, new_name):
    self.name = new_name
    self.save()
    print(f"Thread renamed to {self.name}")
  
  def get_threads_for_user(user_id, name_list=False, print_threads=False):
    # print(f"Fetching threads for user {user_id} with name_list=True")
    threads = OpenAIThread.objects.filter(user=user_id).order_by('-last_accessed')
    thread_objs = [{"name": thread.name, "last_accessed": thread.last_accessed, "threadId": thread.thread_id} for thread in threads]
    if print_threads:
      for thread in thread_objs:
        print(f"Name: {thread['name']}, Last Accessed: {thread['last_accessed']}, Thread ID: {thread['threadId']},")
    return thread_objs
  def delete_thread(self):
      # Delete the thread using the OpenAI API
      openai.beta.threads.delete(thread_id=self.thread_id)
      self.delete()
      print(f"Thread {self.thread_id} deleted")
  
  def fetch_thread_messages(self, print_messages=False):
    print(f"Starting: Fetch Messages for Thread {self.thread_id}...")
    # Fetch messages from OpenAI API
    thread_messages = []
    try:
      has_next_page = True
      while has_next_page:
        response = openai.beta.threads.messages.list(
          thread_id=self.thread_id,
          limit=100,  # Adjust the limit as needed
        )
        messages = response.data
        has_next_page = response.has_more

        for message in messages:
          raw_content = next((obj.text.value for obj in message.content if obj.type == "text"), None)
          if raw_content:
            content = raw_content.split("---context---", 1)[0].strip()
          else:
            content = raw_content
          thread_messages.append({
            'id': message.id,
            'role': message.role,
            'text': content,
            'created_at': message.created_at,
          })

          if print_messages:
            print(f"Message ID: {message.id}")
            print(f"Role: {message.role}")
            print(f"Text: {content[:10]}...")
            print(f"Created At: {message.created_at}")
            print("|------------------------------------------------------------------------------------------------|")
      print(f"Total messages fetched: {len(thread_messages)}")
      # Sort messages by creation date
      thread_messages.sort(key=lambda x: x['created_at'])
      return thread_messages
    except Exception as e:
      print(f"Error fetching messages for thread {self.thread_id}: {e}")
      return []
      

  def get_messages_for_thread(self, print_messages=False):
    print(f"Starting: Get Messages for Thread...")
    queryset = self.messages.all()
    msgs = []
    for q in queryset:
      msgs.append({
        'id': q.message_id,
        'role': q.role,
        'text': q.content,
      })
    if print_messages:
      print(f"thread messages: {msgs}")
    return msgs

class ThreadMessage(models.Model):
  message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  thread = models.ForeignKey(OpenAIThread, on_delete=models.CASCADE, related_name='messages')
  role = models.CharField(max_length=10)  # 'human' or 'ai'
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.role} message in thread {self.thread.thread_id} at {self.created_at}"
  

class MediaStorage(S3Boto3Storage):
  location = ''          # leave empty → store exactly where upload_to returns
  file_overwrite = False # don’t replace existing files with the same key

def user_file_directory_path(instance, filename):
  filename = os.path.basename(filename)  # keep only the file name
  path = f'uploads/user_{instance.user.username}/{filename}'
  print(f'Trying to upload File to Location - {path}')
  return path                              # relative path inside the bucket

class UserFile(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
  filename = models.CharField(max_length=100)
  file = models.FileField(upload_to=user_file_directory_path,max_length=255)
  last_accessed = models.DateTimeField(auto_now_add=True)
  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'filename'], name='unique_filename_per_user')
    ]

  def extract_text(self):
    """
    Extracts all text from the PDF file associated with this UserFile.
    Returns:
      str: The extracted text from the PDF.
    """
    if not self.file or not self.file.name.endswith('.pdf'):
      raise ValueError("The file is not a valid PDF.")

    try:
      # Open the file and read its content
      with self.file.open('rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
          text += page.extract_text()  # Extract text from each page
        return text
    except Exception as e:
      print(f"Error extracting text from PDF: {e}")
      return ""

  def chunk_similarity_scores(self, user_input, embedding_model="text-embedding-3-small", debug=False):
    chunks = self.chunks.all().order_by('chunk_number')
    if debug:
      print(f"Finding most similar chunks for user input: {user_input}")
      print(f"Using embedding model: {embedding_model}")
      print(f"Total chunks available: {len(chunks)}")
    if not chunks:
      print("No chunks available for this file.")
      return []
    
    similiarities = []
    
    for chunk in chunks:
      sim = chunk.compare_to_user_input(user_input, embedding_model)
      similiarities.append((chunk, sim))
    similiarities.sort(key=lambda x: x[1], reverse=True)

    return similiarities

class Chunk(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  file_id = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='chunks')
  chunk_number = models.IntegerField()  # Chunk number in the file
  text = models.CharField(max_length=5000)  # OpenAI file ID if uploaded
  embedding = models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def compare_to_user_input(self, user_input, embedding_model="text-embedding-3-small", debug=True):
    if debug:
      print(f"Comparing chunk {self.chunk_number} to user input: {user_input}")
      print(f"Using embedding model: {embedding_model}")
    # Generate embedding for the user input
    user_embedding = openai.embeddings.create(
      input=user_input,
      model=embedding_model
    ).data[0].embedding
    
    # Calculate cosine similarity
    chunk_embedding = np.array(self.embedding)
    user_embedding = np.array(user_embedding)
    
    similarity = np.dot(chunk_embedding, user_embedding) / (np.linalg.norm(chunk_embedding) * np.linalg.norm(user_embedding))
    with(open('debug.log', 'a') as f):
      f.write(f"Chunk Number: {self.chunk_number}\n")
      f.write(f"Comparing user input \"{user_input}\" - to chunk with text: {self.text[:50]}...\n")
      f.write(f"Similarity Score: {similarity}\n")
    
    if debug:
      print("|------------------------------------------------------------------------------------------------|")
      print(f"Comparing user input \"{user_input}\" to chunk number {self.chunk_number} with text: {self.text[:50]}...")
      print(f"Similarity: {similarity}")
      print("|------------------------------------------------------------------------------------------------|")
    return similarity