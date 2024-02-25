from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer
from .models import ChatModel
import markdown

# Create your views here.

class ChatView(generics.ListCreateAPIView):
    queryset = ChatModel.objects.all()
    serializer_class = ChatSerializer
    
    def post(self, request, *args, **kwargs):
        chat_string = request.data.get('chat_string', '')
        md = markdown.Markdown(extensions=["fenced_code","codehilite"])
        chat_string = md.convert(chat_string)
        processed_chat = chat_string
        return JsonResponse({'processed_chat': processed_chat}) 

    
def GemmaModel(request):
    if request.method == 'POST':
        try:
            question = request.data.get('question')
            model = "https://github.com/llSiddharthll/Bert/blob/main/bert_model.ckpt.data-00000-of-00001"
            result = model(question)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)