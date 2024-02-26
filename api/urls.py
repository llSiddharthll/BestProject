from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('chatapi/', ChatAPIView.as_view(), name='chat'),
    path('aiChat/', AIChatAPIView.as_view(), name='bert')
    
]
