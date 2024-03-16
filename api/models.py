from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    user_name = models.CharField(max_length=25)
    content = models.TextField()
    pfp = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'