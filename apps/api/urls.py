from django.urls import path

from .views import CreateWebhookEvent


urlpatterns = [
    path('new_webhook_event/', CreateWebhookEvent.as_view(), name='create_webhook_event'),
]
