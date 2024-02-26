from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status
from webscout.AI import youChat
import logging

logger = logging.getLogger(__name__)
youChat = youChat()

class ChatAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        chat_serializer = self.get_serializer(data=request.data)
        chat_serializer.is_valid(raise_exception=True)

        chat_string = chat_serializer.validated_data["chat_string"]
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        processed_chat = md.convert(chat_string)

        headers = self.get_success_headers(chat_serializer.data)
        return Response(processed_chat, status=status.HTTP_201_CREATED, headers=headers)


class AIChatAPIView(generics.CreateAPIView):
    serializer_class = BertSerializer

    def create(self, request, *args, **kwargs):
        try:
            bert_serializer = self.get_serializer(data=request.data)
            bert_serializer.is_valid(raise_exception=True)

            question = bert_serializer.validated_data["question"]
            
            # Log the request and question
            logger.info(f"Received request: {request.data}")
            logger.info(f"Question: {question}")

            while True:
                completion = youChat.create(question)
                headers = self.get_success_headers(bert_serializer.data)
                return Response(completion, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)