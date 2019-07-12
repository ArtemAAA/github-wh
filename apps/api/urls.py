from django.urls import path

from .views import WebhookEventList


urlpatterns = [
    path('webhook/events/', WebhookEventList.as_view(), name='api_webhook_events'),
]
