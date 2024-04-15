from django.urls import path
from .views import RedactPIIView

urlpatterns = [
    path('pii-redact', RedactPIIView.as_view(), name='pii-redact'),
]
