from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
# from .views import AudioUploadView

urlpatterns = [

    path('', home, name="home"),
    path('clear-history/', clear_history, name='clear_history'),
    path('chat/', chat_view, name='chat_view'),
    path('api/audio/', get_audio_file, name='audio-file'),
    path('api/upload-audio/', send_audio_to_api, name='upload-audio'),

    # path('voicecall/', voice_call_view, name='voice_call'),
    # path('videocall/', video_call_view, name='video_call')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

