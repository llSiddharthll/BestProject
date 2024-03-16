# serializers.py
from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    chat = serializers.CharField()
    pfp = serializers.CharField()
    user_name = serializers.CharField()

class BertSerializer(serializers.Serializer):
    question = serializers.CharField()

class MarkdownSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=None)