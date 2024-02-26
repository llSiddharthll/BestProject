# views.py
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ChatSerializer, BertSerializer
import markdown
from rest_framework.response import Response
from rest_framework import status
import subprocess


class ChatAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        chat_serializer = self.get_serializer(data=request.data)
        chat_serializer.is_valid(raise_exception=True)

        chat_string = chat_serializer.validated_data["chat_string"]
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        processed_chat = md.convert(chat_string)

        headers = self.get_success_headers(chat_serializer.data)
        return Response(processed_chat, status=status.HTTP_201_CREATED, headers=headers)


class AIChatAPIView(generics.CreateAPIView):
    serializer_class = BertSerializer

    def create(self, request, *args, **kwargs):
        bert_serializer = self.get_serializer(data=request.data)
        bert_serializer.is_valid(raise_exception=True)

        question = bert_serializer.validated_data["question"]
        try:
            command = ["python", "-c", f"from webscout.AI import YepChat; print(YepChat.chat_cli('{question}'))"]
            result = subprocess.run(command, capture_output=True, text=True)

            # Check if the subprocess was successful
            if result.returncode == 0:
                output_lines = result.stdout.strip().splitlines()
                status_code = int(output_lines[0].split()[0])  # Extract status code
                content = ' '.join(output_lines[1:])  # Join the remaining lines as content
                headers = self.get_success_headers(bert_serializer.data)
                return Response({"status_code": status_code, "content": content}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return JsonResponse({"error": result.stderr.strip()}, status=500)

        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": e.stderr.strip()}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)