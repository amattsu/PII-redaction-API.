from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class RedactPIIView(APIView):
    """
    APIView to redact PII using OpenAI's GPT-3.5 model.
    """

    def post(self, request):
        # Получаем текст из запроса
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Вызываем функцию для редакции PII
        redacted_text = self.redact_pii(text)
        if 'error' in redacted_text:
            return Response({'error': redacted_text['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'redacted_text': redacted_text}, status=status.HTTP_200_OK)

    def redact_pii(self, text):
        api_key = os.getenv('OPENAI_API_KEY')
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'prompt': f'Redact PII: {text}',
                'temperature': 0.5,
                'max_tokens': 512
            }

            response = requests.post('https://api.openai.com/v1/engines/gpt-3.5-turbo/completions', json=data,
                                     headers=headers)
            if response.status_code == 200:
                return response.json()['choices'][0]['text']
            else:
                # Обработка ошибок API, включая превышение квоты
                return {'error': response.json().get('error', 'Failed to communicate with OpenAI API')}
        except Exception as e:
            # Логирование для дальнейшего анализа
            print(f"Error processing the request: {str(e)}")
            return {'error': 'Internal Server Error'}


