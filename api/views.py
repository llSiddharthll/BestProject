from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status
from .ChatAI import Gemini

class ChatAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        chat_serializer = self.get_serializer(data=request.data)
        chat_serializer.is_valid(raise_exception=True)

        chat = chat_serializer.validated_data["chat"]
        pfp = chat_serializer.validated_data["pfp"]
        user_name = chat_serializer.validated_data["user_name"]
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        processed_chat = md.convert(chat)

        response = {
            "chat": processed_chat,
            "pfp": pfp,
            "user_name": user_name,
        }
        headers = self.get_success_headers(chat_serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class AIChatAPIView(generics.CreateAPIView):
    serializer_class = BertSerializer

    def create(self, request, *args, **kwargs):
        try:
            bert_serializer = self.get_serializer(data=request.data)
            bert_serializer.is_valid(raise_exception=True)

            question = bert_serializer.validated_data["question"]

            completion = Gemini.chat_cli(question)
            headers = self.get_success_headers(bert_serializer.data)
            return Response(completion, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)