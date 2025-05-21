import os
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ConversationSerializer, UserSerializer
from api.models import Conversation
from api.utils import update_conversation, get_user_conversations, user_id_by_cid

# Function to call the GPT API using LangChain
    

# Django view to handle the assistant API using LangChain
@csrf_exempt
def assistant(request, cid):
    if request.method == "POST":
        try:
            # Parse the user input from the request body
            print("Parsing request body...")
            body = json.loads(request.body)
            user_input = body.get("query", "")
            print(f"User input: {user_input}")

            # Call the LangChain API with the user input
            user_id = user_id_by_cid(cid)
            print(f"User ID: {user_id}")
            ai_response = update_conversation(user_id ,cid, user_input)
            
            print(f"GPT response: {ai_response}")
            #update_conversation(1,1,user_input)
            # Return the GPT response as JSON
            return JsonResponse({"message": ai_response, "status": "success"})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "failure"}, status=500)
    else:
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
                conversation_data = get_user_conversations(user_instance.id)
                print(f"User data: {user_data}")
                return JsonResponse({"message": "Login successful",
                                      "status": "success",
                                      "user": user_data,
                                      "conversations": conversation_data}, status=200)
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
    
class ConversationListView(APIView):

    def get(self, request):
        # Retrieve all conversations
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)




