from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer
from .models import ChatModel
import markdown

# Create your views here.

class ChatView(generics.ListCreateAPIView):
    queryset = ChatModel.objects.all()
    serializer_class = ChatSerializer
    
    def post(self, request, *args, **kwargs):
        chat_string = request.data.get('chat_string', '')
        md = markdown.Markdown(extensions=["fenced_code","codehilite"])
        chat_string = md.convert(chat_string)
        processed_chat = chat_string
        return JsonResponse({'processed_chat': processed_chat}) 