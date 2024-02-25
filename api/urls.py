from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('chatapi/', views.Chat, name='chat'),
    path('bert/', views.Bert, name='bert')
    
]
