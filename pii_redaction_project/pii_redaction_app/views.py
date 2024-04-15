import requests
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

load_dotenv()

class RedactPIIView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        response = self.redact_pii(text)
        return Response({'redacted_text': response}, status=status.HTTP_200_OK)

    def redact_pii(self, text):
        openai_api_key = os.getenv('OPENAI_API_KEY')
        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'prompt': f'Redact PII: {text}',
            'temperature': 0,
            'max_tokens': 150
        }
        response = requests.post('https://api.openai.com/v1/engines/text-davinci-002/completions', json=data,
                                 headers=headers)
        return response.json()['choices'][0]['text']
