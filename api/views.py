from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from .helpers import send_forget_password_mail
from .translation_utils import translate_to_nepali
from .translation_utils import translate_to_english
from llama_index import GPTVectorStoreIndex
from .gpt import *
import openai
import psutil
import shutil
import os
from elevenlabs import generate
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http.HttpRequest import request
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import os
import shutil
import requests
from django.http import JsonResponse, FileResponse
from .translation_utils import translate_to_nepali, translate_to_english  # Assuming you have translation functions
from gradio_client import Client  


gradio_client = Client("https://elevenlabs-tts.hf.space/")

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium"
HEADERS = {"Authorization": "Bearer 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"}

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def home(request):
    return Response(status=status.HTTP_200_OK)



# Other views (chat_view, voice_call_view, etc.) can be similarly converted to use DRF.

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def chat_view(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat_history = request.session['chat_history']

    if request.method == 'POST':
        user_message = request.data.get('message')
        selected_language = request.data.get('language')

        if selected_language == 'nepali':
            print("User input message:", user_message)
            user_message_server = translate_to_english(user_message) # This contains the message that is translated (if user inputs तिम्रो नाम के हो?, then "What is your name?" is stored here.)
            print("Translated text that is sent to AI:", user_message_server)
            # ai_chat_response = ask_ai(user_message) 
            # ai_chat_response = translate_to_nepali(ai_chat_response)
            # chatbot_response = ai_chat_response
            chatbot_response="hehe"
        elif selected_language =='english':
            # ai_chat_response = ask_ai(user_message)
            # ai_chat_response= translate_to_english(ai_chat_response)
            # chatbot_response = ai_chat_response
            chatbot_response= "hehe"

        # Save the chat history using the original Django HttpRequest
        save_chat_history(request._request, user_message, chatbot_response)

    # Handle GET requests if needed
    # Add your logic here if necessary

    return Response({'chat_history': chat_history})

@api_view(['POST'])
def save_chat_history(request, user_message, chatbot_response):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat_history = request.session['chat_history']
    chat_history.append(('user', user_message))
    chat_history.append(('Bot', chatbot_response))
    request.session['chat_history'] = chat_history

    return Response({'message': 'Chat history saved successfully.'})





@api_view(['POST'])
def clear_history(request):
    request.session['chat_history'] = []
    return Response({'message': 'Chat history cleared successfully.'})

@api_view(['POST'])
def send_audio(request):
    if request.method == 'POST':
        audio_data = request.FILES['audio_file'].read()
        response = send_audio_to_api(audio_data)
        selected_language = request.data.get('language')
        
        # Rest of your code remains unchanged...

        return Response(response)
    else:
        return Response({'error': 'Invalid Request'}, status=400)

@api_view(['GET'])
def serve_audio(request):
    file_path = r'../audio/audio.mp3'
    audio_file = open(file_path, 'rb')
    response = FileResponse(audio_file)
    return response

@api_view(['GET'])
def call_view(request):
    return render(request, 'audiorecorderapp/index1.html')

@api_view(['POST'])
def send_audio_to_api(request):
    if request.method == 'POST':
        audio_data = request.FILES['audio_file'].read()
        response = requests.post(API_URL, headers=HEADERS, data=audio_data)
        return Response(response.json())
    else:
        return Response({'error': 'Invalid Request'}, status=400)

@api_view(['POST'])
def predict_transcript(request):
    if request.method == 'POST':
        transcript = request.data.get('transcript')
        selected_language = request.data.get('selected_language', 'english')

        print("selected_language:", selected_language)

        if selected_language == 'nepali':
            transcript1 = translate_to_nepali(transcript)
        elif selected_language == 'english':
            transcript1 = translate_to_english(transcript)
        else:
            transcript1 = transcript

        print(transcript1)

        result = gradio_client.predict(transcript1, "Rachel", fn_index=0)

        return Response({'result': result})
    else:
        return Response({'error': 'Invalid Request'}, status=400)