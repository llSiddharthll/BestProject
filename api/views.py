
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer, MarkdownSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status
from .ChatAI import Gemini
from django.http import JsonResponse
from django.utils import timezone
from .models import Message
from rest_framework.views import APIView

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

        message = Message.objects.create(user_name=user_name, content=chat, pfp=pfp)
        message.save
        response = {
            "chat": processed_chat,
            "pfp": pfp,
            "user_name": user_name,
        }
        headers = self.get_success_headers(chat_serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

def poll_messages(request):
    last_poll_time_str = request.GET.get('last_poll_time', None)

    if last_poll_time_str:
        try:
            last_poll_time = timezone.datetime.fromisoformat(last_poll_time_str)
        except ValueError:
            last_poll_time = None
    else:
        last_poll_time = None

    # Query for messages created after the last poll time
    if last_poll_time:
        messages = Message.objects.filter(created_at__gt=last_poll_time)
    else:
        # If no last_poll_time, get all messages (for the initial poll)
        messages = Message.objects.all()

    # Convert messages to a list of dictionaries
    messages_data = [{'user_name': msg.user_name, 'content': msg.content, 'pfp': msg.pfp, 'created_at': msg.created_at} for msg in messages]

    return JsonResponse({'messages': messages_data})

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
        
class MarkdownAPIView(APIView):
    def get(self, request):
        serializer = MarkdownSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        processed_text = md.convert(text)
        return Response({'processed_text': processed_text})