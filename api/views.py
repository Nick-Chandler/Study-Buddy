import os, json, uuid
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, OpenAIThreadSerializer, UserFileSerializer
from api.models import OpenAIAssistant, OpenAIThread, ThreadMessage, UserFile
from api import gpt_assistant, gpt_assistant2, utils
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import openai

    
@csrf_exempt
def assistant(request, user_id, thread_id):

    if request.method == 'POST':
      print(f"Calling Assistant for User ID: {user_id}, Thread Id: {thread_id}")
      user_input = request.POST.get('user_input', '')
      file_array = request.FILES.getlist('files')
      document = request.FILES.getlist('document')

      print(f"User input: {user_input}")
      print(f"Files received: {len(file_array)} files")
      thread = OpenAIThread.objects.get(thread_id=thread_id, user_id=user_id)
      thread.save()
      human_message = ThreadMessage.objects.create(thread=thread, role="human", content=user_input)
      try:
          assistant_id = OpenAIAssistant.objects.filter(model="gpt-4.1-mini").first().assistant_id
          print("Calling assistant function...")
          gpt_response = gpt_assistant.run_assistant(user_id, thread_id, user_input, file_array, document, assistant_id=assistant_id)
          ai_message = ThreadMessage.objects.create(thread=thread, role="ai", content=gpt_response)
          print(f"GPT Response: {gpt_response}")
          current_document = utils.get_most_recent_userfile(user_id)
          most_similar_pages = current_document.most_similar_chunks(user_input,n=5,debug=True)
          return JsonResponse({"message": gpt_response,
                                "status": "success"}, status=200)
      except Exception as e:
          return JsonResponse({"error": str(e), "status": "failure"}, status=500)
        
def assistant2(request, user_id, thread_id):
      try:
        user_input = request.POST.get('user_input', '')
        print(f"User input: {user_input}")
        document_name = request.POST.get('document_name', None)
        print(f"Document name: {document_name}")
        assistant = OpenAIAssistant.objects.filter(model="gpt-4o-mini").first()
        gpt_response = gpt_assistant2.run_assistant2(user_id, thread_id, user_input, assistant=assistant, max_prompt_tokens=20000, debug=True)
        return JsonResponse({"message": gpt_response,
                                "status": "success"}, status=200)
      except Exception as e:
        print(f"Error in assistant_2: {e}")
        return JsonResponse({"error": str(e), "status": "failure"}, status=500)


    
def get_user_thread_list(request, user_id):
    print(f"Fetching thread list for user {user_id}")
    try:
      user_threads = OpenAIThread.get_threads_for_user(user_id, name_list=True, print_threads=False)
    except Exception as e:
      print(f"Error fetching threads for user {user_id}: {e}")
      return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse(user_threads, safe=False)

def get_user_thread_messages(request, user_id, thread_id):
    print(f"Fetching messages for user - {user_id}: | thread index - {thread_id}")
    if not thread_id:
      print(f"Thread id {thread_id} not found for user: {user_id}")
      return JsonResponse({"error": "Thread not found", "status": "failure"}, status=404)
    
    print(f"Calling fetch_thread_messages with thread ID: {thread_id}")
    # thread = OpenAIThread.objects.get(thread_id=thread_id)
    # thread_msgs = thread.get_messages_for_thread(print_messages=False)
    # thread_msgs = ThreadMessage.objects.filter(thread__thread_id=thread_id).order_by('created_at')
    client = openai.OpenAI()
    thread_messages = []
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        thread_messages = []
        has_next_page = True
        while has_next_page:
            for index, message in enumerate(messages.data):
                # print(f"Message {index}: {message}")
                text = next(
                (part.text.value for part in message.content if part.type == "text"),
                ""  # default to empty string if no text part
                )
                thread_messages.insert(0,{
                    'id': message.id,
                    'role': message.role,
                    'text': text
                })
                # print(f"Message {index} added: {thread_messages[-1]}")
            has_next_page = messages.has_more
            # print(f"Has next page: {has_next_page}")
            if has_next_page:
                print(f"Fetching next page of messages for thread {thread_id}")
                messages = client.beta.threads.messages.list(thread_id=thread_id, after=messages.data[-1].id)
        print(f"Fetched {len(thread_messages)} messages for thread {thread_id}")
        # for msg in thread_messages:
        #     print("Text:", msg['text'], "Role:", msg['role'],"Message ID:", msg['id'])
    except Exception as e:
        print(f"Error fetching messages for thread {thread_id}: {e}") 
        return JsonResponse({"error": "Failed to fetch messages", "status": "failure"}, status=500)
    print(f"Total messages fetched: {len(thread_messages)}")
    # for msg in thread_messages:
    #     print("Message ID:", msg['id'], "Role:", msg['role'], "Text:", msg['text'])
    return JsonResponse(thread_messages, safe=False)


@csrf_exempt
def upload_document(request, user_id):
    print(f"Upload document request received for user {user_id}")
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        try:
            if not request.FILES or 'document' not in request.FILES:
                print("No files found in the request")
                return JsonResponse({"error": "No files found", "status": "failure"}, status=400)
            print(f"Uploading file for user {user_id}")
            document = request.FILES.get('document')
            document_name = document.name
            print(f"Document received: {document_name}")
            if not document:
                print("No document or document name provided")
                return JsonResponse({"error": "No file found", "status": "failure"}, status=400)
            
            try:
                print(f"Creating UserFile instance for user {user_id} with filename {document_name}")
                file_instance = UserFile.objects.create(user_id=user_id, filename=document_name, file=document)
                print("UserFile instance created successfully")
                status = 201
                return JsonResponse({"message": "File uploaded successfully",
                                  "status": "success",
                                  "filename": document_name}, status=status)
            except IntegrityError as e:
                print(f"File with this name already exists: {e}")
                file_instance = UserFile.objects.get(user_id=user_id, filename=document_name)
                file_instance.save()
                status = 200
                return JsonResponse({"message": "File uploaded successfully, but a file with this name already exists",
                                  "status": "success",
                                  "filename": document_name}, status=status)
        except Exception as e:
            print(f"Error uploading file for user {user_id}: {e}")
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def create_thread_for_user(request, user_id, name="Untitled Thread"):
    if request.method == 'POST':
        try: 
            print(f"Creating thread for user {user_id}")
            user_instance = User.objects.get(id=user_id)
            new_thread = OpenAIThread.objects.create(user=user_instance, name=name)
            print(f"Thread created: {new_thread.thread_id} for user {user_id} with name {name}")
        except Exception as e:
            print(f"Error creating thread for user {user_id}: {e}")
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
        return JsonResponse({"message": "Thread created successfully",
                                "status": "success",
                                "threadId": new_thread.thread_id,
                                "name": name}, status=201)

@csrf_exempt
def rename_thread(request, user_id, thread_id, new_name):
    if request.method == 'POST':
        try:
            print(f"Renaming thread {thread_id} for user {user_id} to {new_name}")
            thread = OpenAIThread.objects.get(thread_id=thread_id, user_id=user_id)
            thread.rename_thread(new_name)
            return JsonResponse({"message": "Thread renamed successfully",
                                  "status": "success",
                                  "newThreadName" : new_name}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def delete_thread(request, user_id, thread_id):
    if request.method == 'POST':
        try:
            print(f"Deleting thread {thread_id} for user {user_id}")
            deleted_thread_name = utils.delete_thread(user_id, thread_id)
            return JsonResponse({"message": "Thread deleted successfully",
                                  "status": "success",
                                  "deletedThreadName" : deleted_thread_name}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_file_url(request):
    if request.method == 'GET':
        user = User.objects.get(id=1)
        user_file = UserFile.objects.filter(user=user).first()
        file_url = request.build_absolute_uri(user_file.file.url)
        return JsonResponse({'file_url': file_url}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    

def firebase_login_view(request, email):
    if request.method == "GET":
        user, created = User.objects.get_or_create(username=email)
        threads = OpenAIThread.get_threads_for_user(user.id, name_list=True, print_threads=True)
        print(f"User found: {user.username}")
        return JsonResponse({"message": "User found",
                              "status": "success",
                              "username": user.username,
                              "userId": user.id}, status=200)


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_instance = User.objects.get(username=username)
                # user_data = UserSerializer(user_instance).data
                username = user_instance.username
                user_id = user_instance.id
                threads = OpenAIThread.get_threads_for_user(user_id, name_list=True, print_threads=True)
                last_accessed_thread = utils.get_last_accessed_thread(user_instance.id)
                print("Last Accesed Thread Type:", type(last_accessed_thread))
                # print(f"User data: {user_data}")
                return JsonResponse({"message": "Login successful",
                                      "status": "success",
                                      "username": username,
                                      "userId": user_id,
                                      "threads": threads,
                                      "lastAccessedThread": last_accessed_thread}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials",
                                      "status": "failure"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        try:
            # Log out the user
            logout(request)
            return JsonResponse({"message": "Logout successful", "status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            # Parse the request body
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            email = data.get("email", "")  # Optional email field

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists",
                                      "status": "failure"}, status=400)

            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Automatically log in the user after registration
            login(request, user)
            user_instance = User.objects.get(username=username)
            user_data = UserSerializer(user_instance).data

            return JsonResponse({"message": "Registration successful",
                                  "status": "success",
                                  "user": user_data}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
@csrf_exempt
def conversation_view(request, cid):
    if request.method == "GET":
        try:
            print(request)
            return JsonResponse({"message": "GET request received",
                                  "status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    
    
class OpenAIThreadListView(APIView):

    def get(self, request):
        # Retrieve all conversations
        Threads = OpenAIThread.objects.all()
        serializer = OpenAIThreadSerializer(Threads, many=True)
        return Response(serializer.data)


class AllUserFilesView(APIView):

    def get(self, request):
        # Retrieve all user files
        user_files = UserFile.objects.all()
        serializer = UserFileSerializer(user_files, many=True)
        return Response(serializer.data)
