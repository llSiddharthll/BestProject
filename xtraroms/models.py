from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class CustomROM(models.Model):
    name = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    credits = models.CharField(null=True, max_length=50)
    image = models.ImageField(upload_to="images")
    link = models.URLField(max_length=225)
    details = models.TextField()
    upload_date = models.DateField(null=True, blank=True) # use auto_now instead of auto_now_add
    boot_link = models.URLField(max_length=225, null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_roms',default=0)
    class Meta:
        db_table = 'xtraroms_api_roms'


    def __str__(self):
        return self.name
    

class CustomMOD(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    credits = models.CharField(null=True, max_length=50)
    link = models.URLField()
    details = models.TextField()
    upload_date = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_mods',default=0)
    class Meta:
        db_table = 'xtraroms_api_mods'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_authorized = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_picture/", null=True, blank=True)
    status_choices = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("away", "Away"),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default="offline")
    last_seen = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'xtraroms_api_userprofile'

    def __str__(self):
        return self.user.username
    
