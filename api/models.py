from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import storages
import uuid  # To generate unique conversation IDs
import openai

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
    last_accessed = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Thread for {self.user.username}: {self.thread_id}"
    
    def rename_thread(self, new_name):
        self.name = new_name
        self.save()
        print(f"Thread renamed to {self.name}")
    
    def get_threads_for_user(user_id, name_list=False, print_threads=False):
      user = User.objects.get(id=user_id)
      if not name_list:
        return OpenAIThread.objects.filter(user_id=user_id).order_by('-last_accessed')
      else:
        # print(f"Fetching threads for user {user_id} with name_list=True")
        threads = OpenAIThread.objects.filter(user=user).order_by('-last_accessed')
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
  

def user_file_directory_path(instance, filename):
  return f"uploads/user_{instance.user.username}/{filename}"

class UserFile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
  filename = models.CharField(max_length=100)
  file = models.FileField(storage=storages["s3"], upload_to=user_file_directory_path,max_length=255)
  last_accessed = models.DateTimeField(auto_now_add=True)
  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'filename'], name='unique_filename_per_user')
    ]


