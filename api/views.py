
# views.py
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status
import requests

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    formatted_payload = f"""
        GPT4 Correct User: Hello<|end_of_turn|>
        GPT4 Correct Assistant: Hi<|end_of_turn|>
        GPT4 Correct User: What is your name?<|end_of_turn|>
        GPT4 Correct Assistant: My name is "Itachi Uchiha" of the village "leaf", I am a conversational bot made by Siddharth<|end_of_turn|>
        GPT4 Correct User: {payload}<|end_of_turn|>
        GPT4 Correct Assistant: 
        """
    response = requests.post(API_URL, headers=headers, json={"inputs": formatted_payload})
    return response.json()
            
class ChatAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        chat_serializer = self.get_serializer(data=request.data)
        chat_serializer.is_valid(raise_exception=True)
        
        chat_string = chat_serializer.validated_data['chat_string']
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        processed_chat = md.convert(chat_string)
        
        headers = self.get_success_headers(chat_serializer.data)
        return Response(processed_chat, status=status.HTTP_201_CREATED, headers=headers)


class BertAPIView(generics.CreateAPIView):
    serializer_class = BertSerializer

    def create(self, request, *args, **kwargs):
        bert_serializer = self.get_serializer(data=request.data)
        bert_serializer.is_valid(raise_exception=True)

        question = bert_serializer.validated_data['question']
        try:
            output = query(question)
            
            headers = self.get_success_headers(bert_serializer.data)
            return Response(output, status=status.HTTP_201_CREATED, headers=headers)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
