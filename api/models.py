from django.db import models

# Create your models here.

class ChatModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)