from django.urls import path, include

urlpatterns = [
    path('api/', include('pii_redaction_app.urls')),
]
