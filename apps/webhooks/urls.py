from django.urls import path

from .views import WebhooksView


urlpatterns = [
    path('', WebhooksView.as_view(), name='webhooks'),
]
