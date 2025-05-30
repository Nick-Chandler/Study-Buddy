import os
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, OpenAIThreadSerializer, UserFileSerializer
from api.models import OpenAIThread, ThreadMessage, UserFile
from api import gpt_assistant, utils

    
@csrf_exempt
def assistant(request, user_id, thread_id):

    if request.method == 'POST':
        print(f"Assistant User ID: {user_id}, Thread Id: {thread_id}")
        print("Decoding request body...")
        body_unicode = request.body.decode('utf-8')
        print(f"Request body: {body_unicode}")
        print("Convering to JSON...")
        body_data = json.loads(body_unicode)
        print(f"Body data: {body_data}")
        print("Retrieving user input...")
        user_input = body_data.get('user_input', '')
        print(f"User input: {user_input}")
        thread = OpenAIThread.objects.get(thread_id=thread_id, user_id=user_id)
        human_message = ThreadMessage.objects.create(thread=thread, role="human", content=user_input)
        try:
            print("Calling assistant function...")
            gpt_response = gpt_assistant.run_assistant(user_id, thread_id, user_input)
            ai_message = ThreadMessage.objects.create(thread=thread, role="ai", content=gpt_response)
            print(f"GPT Response: {gpt_response}")
            print(f"Type of GPT Response: {type(gpt_response)}")

            return JsonResponse({"message": gpt_response,
                                "status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    
def get_user_thread_list(request, user_id):
    print(f"Fetching thread list for user {user_id}")
    user_threads = OpenAIThread.get_threads_for_user(user_id, name_list=True)
    print(f"User threads: ", user_threads)

    return JsonResponse(user_threads, safe=False)

def get_user_thread_messages(request, user_id, thread_id):
    print(f"Fetching messages for user {user_id}: thread index {thread_id}")
    if not thread_id:
        print(f"Thread id {thread_id} not found for user: {user_id}")
        return JsonResponse({"error": "Thread not found", "status": "failure"}, status=404)
    print(f"Calling fetch_thread_messages with thread ID: {thread_id}")
    thread = OpenAIThread.objects.get(thread_id=thread_id)
    thread_msgs = thread.get_messages_for_thread()
    # thread_msgs = ThreadMessage.objects.filter(thread__thread_id=thread_id).order_by('created_at') 
    print(f"thread messages: {thread_msgs}")
    return JsonResponse(thread_msgs, safe=False)


@csrf_exempt
def upload_file(request, user_id):
    if request.method == 'POST':
        try:
            print(f"Uploading file for user {user_id}")
            file = request.FILES.get('file')
            filename = request.POST.get('filename')
            if not file or not filename:
                return JsonResponse({"error": "No file found", "status": "failure"}, status=400)

            print(f"File received: Filename: {filename}")
            
            file_instance = UserFile.objects.create(user_id=user_id, filename=filename, file=file)
            return JsonResponse({"message": "File uploaded successfully",
                                  "status": "success",
                                  "filename": filename}, status=201)
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
                user_data = UserSerializer(user_instance).data
                thread_names = utils.get_user_thread_list(user_instance.id)
                last_conversation = utils.get_last_user_conversation(user_instance.id)
                print(f"User data: {user_data}")
                return JsonResponse({"message": "Login successful",
                                      "status": "success",
                                      "user": user_data,
                                      "conversations": thread_names,
                                      "lastConversation": last_conversation}, status=200)
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
