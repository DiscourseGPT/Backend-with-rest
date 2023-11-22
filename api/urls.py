from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    path('', home, name="home"),
    path('clear-history/', clear_history, name='clear_history'),
    path('chat/', chat_view, name='chat_view'),
    # path('voicecall/', voice_call_view, name='voice_call'),
    # path('videocall/', video_call_view, name='video_call')
]
