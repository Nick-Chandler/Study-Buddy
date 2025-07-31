import os, json, uuid, openai
from django.http import FileResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, OpenAIThreadSerializer, UserFileSerializer
from api.models import OpenAIAssistant, OpenAIThread, ThreadMessage, UserFile
from api import gpt_assistant, gpt_assistant2, gpt_assistant3, utils
from django.shortcuts import get_object_or_404

    
@csrf_exempt
def assistant(request, user_id, thread_id):
    if request.method == 'POST':
      print(f"Calling Assistant for User ID: {user_id}, Thread Id: {thread_id}")
      user_input = request.POST.get('user_input', '')
      document_name = request.POST.get('document_name', None)
      print("Document Provided:", document_name)
      document = UserFile.objects.filter(user_id=user_id, filename=document_name).first() if document_name else None

      print(f"User input: {user_input}")
      thread = OpenAIThread.objects.get(thread_id=thread_id, user_id=user_id)
      thread.save()
      human_message = ThreadMessage.objects.create(thread=thread, role="human", content=user_input)
      try:
          assistant_id = OpenAIAssistant.objects.filter(model="gpt-4.1-mini").first().assistant_id
          print("Calling assistant function...")
          gpt_response = gpt_assistant.run_assistant(user_id, thread_id, user_input, user_file=document, assistant_id=assistant_id)
          ai_message = ThreadMessage.objects.create(thread=thread, role="ai", content=gpt_response)
          print(f"GPT Response: {gpt_response}")
          current_document = utils.get_most_recent_userfile(user_id)
          most_similar_pages = current_document.most_similar_chunks(user_input,n=5,debug=True)
          return JsonResponse({"message": gpt_response,
                                "status": "success"}, status=200)
      except Exception as e:
          return JsonResponse({"error": str(e), "status": "failure"}, status=500)

@csrf_exempt      
def assistant2(request, user_id, thread_id):
      try:
        user_input = request.POST.get('user_input', '')
        print(f"User input: {user_input}")
        document_name = request.POST.get('document_name', None)
        print(f"Document name: {document_name}")
        assistant = OpenAIAssistant.objects.filter(model="gpt-4.1-mini").first()
        gpt_response = gpt_assistant2.run_assistant(user_id, thread_id, user_input, assistant, document_name, max_prompt_tokens=20000, debug=True)
        return JsonResponse({"message": gpt_response,
                                "status": "success"}, status=200)
      except Exception as e:
        print(f"Error in assistant_2: {e}")
        return JsonResponse({"error": str(e), "status": "failure"}, status=500)
      
@csrf_exempt      
def assistant3(request, user_id, thread_id):
    try:
        user_input = request.POST.get('user_input', '')
        print(f"User input: {user_input}")
        document_name = request.POST.get('document_name', None)
        user_file = UserFile.objects.filter(user_id=user_id, filename=document_name).first() if document_name else None
        print(f"Document name: {document_name}")
        gpt_response = gpt_assistant3.run_assistant(user_id, thread_id, user_input, user_file, max_prompt_tokens=20000)
        return JsonResponse({"message": gpt_response,
                                "status": "success"}, status=200)
    except Exception as e:
        print(f"Error in assistant_2: {e}")
        return JsonResponse({"error": str(e), "status": "failure"}, status=500)



    
def get_user_thread_list(request, user_id):
    print(f"Fetching thread list for user {user_id}")
    try:
      user_threads = OpenAIThread.get_threads_for_user(user_id, name_list=True, print_threads=True)
      print(user_threads)
    except Exception as e:
      print(f"Error fetching threads for user {user_id}: {e}")
      return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    return JsonResponse(user_threads, safe=False)

def get_user_thread_messages(request, user_id, thread_id):
    print(f"Fetching messages for user - {user_id}: | thread index - {thread_id}")
    
    print(f"Calling fetch_thread_messages with thread ID: {thread_id}")
    try:
        thread = OpenAIThread.objects.get(thread_id=thread_id, user_id=user_id)
        thread_messages = thread.fetch_thread_messages(print_messages=True)
        print(f"Fetched {len(thread_messages)} messages for thread {thread_id}")

    except Exception as e:
        print(f"Error fetching messages for thread {thread_id}: {e}") 
        return JsonResponse([],safe=False, status=500)
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
            document = request.FILES.get('document')
            if not document:
                print("No document or document name provided")
                return JsonResponse({"error": "No file found", "status": "failure"}, status=400)
            print(f"Uploading file for user {user_id}")
            print(f"Document type: {type(document)}")
            document_name = document.name
            print(f"Document received: {document_name}")
            
            print(f"Creating UserFile instance for user {user_id} with filename {document_name}")
            user = User.objects.get(id=user_id)
            print(f"Document Type:", type(document))
            file_instance = UserFile.objects.filter(user=user, filename=document_name).first()
            if not file_instance:
                file_instance = UserFile.objects.create(user=user, filename=document_name, file=document)
            file_instance.save()
            print("UserFile instance created successfully")
            return JsonResponse({"message": "File uploaded successfully",
                                "status": "success",
                                "filename": document_name}, status=201)
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
                last_accessed_file = utils.get_most_recent_userfile(user_instance.id).id
                print("Last Accessed File ID:", last_accessed_file)
                return JsonResponse({"message": "Login successful",
                                      "status": "success",
                                      "username": username,
                                      "userId": user_id,
                                      "threads": threads,
                                      "lastAccessedThread": last_accessed_thread,
                                      "lastAccessedFile" : last_accessed_file}, status=200)
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
def retrieve_userfile(request, file_id):
    # Retrieve the UserFile object by ID
    user_file = get_object_or_404(UserFile, id=file_id)

    # Get the file path from the storage backend
    file_path = user_file.file.path  # This works for local storage; for S3, use user_file.file.open()

    # Return the file as a FileResponse
    try:
        response = FileResponse(open(file_path, 'rb'), as_attachment=False, filename=user_file.filename)
        return response
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
