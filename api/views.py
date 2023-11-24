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
import json
from django.conf import settings



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

# @api_view(['POST'])
# def send_audio_to_api(request):
#     if request.method == 'POST':
#         audio_data = request.FILES['audio_file'].read()
#         response = requests.post(API_URL, headers=HEADERS, data=audio_data)
#         # print(response.text)
#         response_json = json.loads(response.text)

#         # Extract the value associated with the key "text"
#         extracted_text = response_json.get("text", "")

#         # Remove leading and trailing whitespaces
#         extracted_text = extracted_text.strip()

#         # Print or use the extracted text
#         print(extracted_text)
#         response1 = predict_transcript(extracted_text,"english")
#         print(response1)
#         destination_path = os.path.join(settings.BASE_DIR,'media')
#         try:
#             if os.path.exists(destination_path):
#                 shutil.rmtree(destination_path)
#             os.makedirs(destination_path)
#         except Exception as e:
#             print(f"Failed to clear the audio folder: {e}")
#         try:
#             shutil.move(response1, destination_path)
#             print(destination_path)
#             new_audio_file_path = os.path.join(destination_path, "audio.mp3")
#             response['audio_processed'] = True
#             response['audio_file_path'] = new_audio_file_path
        
            
#         except Exception as e:
#             print(f"Failed to move audio file")
#         response['audio_processed'] = True 


#         return Response(response.json())
        
#     else:
#         return Response({'error': 'Invalid Request'}, status=400)


@api_view(['POST'])
def send_audio_to_api(request):
    if request.method == 'POST':
        try:
            audio_file = request.FILES['audio_file']
            audio_data = audio_file.read()
        except KeyError:
            return Response({'error': 'No audio file provided'}, status=400)

        response = requests.post(API_URL, headers=HEADERS, data=audio_data)

        try:
            response_json = response.json()
            extracted_text = response_json.get("text", "").strip()
        except json.JSONDecodeError:
            # Handle the case where the response is not JSON
            return Response({'error': 'Invalid response from the API'}, status=500)

        print(f"Extracted Text: {extracted_text}")

        response1 = predict_transcript(extracted_text, "english")
        print(f"Prediction Response: {response1}")

        destination_path = os.path.join(settings.BASE_DIR, 'media')

        try:
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)
            os.makedirs(destination_path)
        except Exception as e:
            print(f"Failed to clear the audio folder: {e}")

        try:
            shutil.move(response1, destination_path)
            print(f"Audio moved to: {destination_path}")
            new_audio_file_path = os.path.join(destination_path, "audio.mp3")
        except Exception as e:
            print(f"Failed to move audio file: {e}")
            return Response({'error': 'Failed to process audio'}, status=500)

        # Update the response data
        response_data = {
            'audio_processed': True,
            'audio_file_path': new_audio_file_path
        }

        return Response(response_data)
        
    else:
        return Response({'error': 'Invalid Request'}, status=400)
    
def predict_transcript(transcript, selected_language):
    print("selected_language:", selected_language)
    # ai_response=ask_ai(transcript)
    if selected_language == 'nepali':
        transcript1 = translate_to_nepali(transcript)
    elif selected_language == 'english':
        transcript1 = translate_to_english(transcript)
    else:
        transcript1 = transcript
    print(transcript1)
    result = gradio_client.predict(
        # response1,
        transcript1,
        "Rachel",
        fn_index=0
    )
    return result


# @api_view(['POST'])
# def predict_transcript(request):
#     if request.method == 'POST':
#         transcript = request.data.get('transcript')
#         selected_language = request.data.get('selected_language', 'english')

#         print("selected_language:", selected_language)

#         if selected_language == 'nepali':
#             transcript1 = translate_to_nepali(transcript)
#         elif selected_language == 'english':
#             transcript1 = translate_to_english(transcript)
#         else:
#             transcript1 = transcript

#         print(transcript1)

#         result = gradio_client.predict(transcript1, "Rachel", fn_index=0)

#         return Response({'result': result})
#     else:
#         return Response({'error': 'Invalid Request'}, status=400)
    
from django.http import FileResponse
from rest_framework.views import APIView

@api_view(['GET'])
def get_audio_file(request):
    try:
        audio_file_path = "media/audio.mp3"  # Replace with the actual path
        return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mp3')
    except Exception as e:
        print(f"Error: {e}")

    
# from rest_framework.parsers import FileUploadParser
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from django.http import HttpResponse
# from django.conf import settings
# from rest_framework.parsers import FileUploadParser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.views.decorators.csrf import csrf_exempt

# import os

# @csrf_exempt
# def upload_audio(request):
#     if request.method == 'OPTIONS':
#         response = HttpResponse()
#         response.setHeader("Access-Control-Allow-Origin", "*");
#         response.setHeader("Access-Control-Allow-Credentials", "true");
#         response.setHeader("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
#         response.setHeader("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");

#         return response

#     if request.method == 'POST':
#         try:
#             file_obj = request.FILES.get('audio')
#             if not file_obj:
#                 return Response({'error': 'No audio file provided.'}, status=400)

#             # Specify the folder where you want to save the audio file
#             upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
#             os.makedirs(upload_folder, exist_ok=True)

#             # Create a unique filename or use the original filename
#             filename = os.path.join(upload_folder, file_obj.name)

#             # Ensure the file has an MP3 extension
#             if not filename.endswith('.mp3'):
#                 filename += '.mp3'

#             # Save the file to the specified folder
#             with open(filename, 'wb') as destination:
#                 for chunk in file_obj.chunks():
#                     destination.write(chunk)

#             return Response({'message': 'Audio file received and saved successfully.'})

#         except Exception as e:
#             return Response({'error': str(e)}, status=400)

#     return HttpResponse('Method not allowed', status=405)