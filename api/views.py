import os
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from api.models import Conversation, Message
from api.utils import store_message, init_llm, update_conversation

# Function to call the GPT API using LangChain
    

# Django view to handle the assistant API using LangChain
@csrf_exempt
def assistant(request):
    if request.method == "POST":
        try:
            # Parse the user input from the request body
            print("Parsing request body...")
            body = json.loads(request.body)
            user_input = body.get("query", "")
            print(f"User input: {user_input}")

            # Call the LangChain API with the user input
            ai_response = update_conversation(1, "a158919f-218b-45cb-a303-a832a3b89716", user_input)
            
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
                print(f"User data: {user_data}")
                return JsonResponse({"message": "Login successful",
                                      "status": "success",
                                      "user": user_data}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials",
                                      "status": "failure"}, status=401)
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
    
class ConversationListView(APIView):

    def get(self, request):
        # Retrieve all conversations
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)




