
# views.py
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status

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
            # Your model logic for Bert goes here
            model = "https://github.com/llSiddharthll/Bert/blob/main/bert_model.ckpt.data-00000-of-00001"
            result = model(question)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
