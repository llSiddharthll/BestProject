# serializers.py
from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    chat = serializers.CharField()
    pfp = serializers.ImageField()
    user_name = serializers.CharField()

class BertSerializer(serializers.Serializer):
    question = serializers.CharField()
