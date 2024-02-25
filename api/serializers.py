# serializers.py
from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    chat_string = serializers.CharField()

class BertSerializer(serializers.Serializer):
    question = serializers.CharField()
