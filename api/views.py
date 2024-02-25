
# views.py
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status
import requests

from transformers import AutoTokenizer, AutoModelForCausalLM


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
            output = gemma(question)
            headers = self.get_success_headers(bert_serializer.data)
            return Response(output, status=status.HTTP_201_CREATED, headers=headers)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def gemma(input):
        tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
        model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")

        input_text = input
        input_ids = tokenizer(input_text, return_tensors="pt")

        outputs = model.generate(**input_ids)
        return tokenizer.decode(outputs[0])