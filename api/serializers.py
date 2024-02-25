from rest_framework.serializers import Serializer
from .models import ChatModel

class ChatSerializer(Serializer):
    model = ChatModel
    fields = '__all__'