from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from dotenv import load_dotenv
import logging
import requests
import os

logger = logging.getLogger(__name__)
load_dotenv()

class RedactPIIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get text from the request body
        text = request.data.get('text', '')
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Attempt to redact PII from the text
        redacted_text = self.redact_pii(text)
        if 'error' in redacted_text:
            return Response({'error': redacted_text['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'redacted_text': redacted_text}, status=status.HTTP_200_OK)

    def redact_pii(self, text):
        # Fetch API key from environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("API key not available")
            return {'error': 'API key not available'}

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {"role": "user", "content": f"Redact PII: {text}"},
            ],
            'max_tokens': 512
        }

        # Post request to OpenAI API
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                # Handle errors from the API response
                error_msg = response.json().get('error', 'Failed to communicate with OpenAI API')
                logger.error(f"API response error: {error_msg}")
                return {'error': error_msg}
        except Exception as e:
            logger.error(f"Error sending request to OpenAI: {str(e)}")
            return {'error': f'Internal Server Error: {str(e)}'}
