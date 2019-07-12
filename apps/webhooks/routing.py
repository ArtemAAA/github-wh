from django.conf.urls import url

from .consumers import WebhookEventsConsumer


websocket_urlpatterns = [
    url(r'^ws/webhooks/events/$', WebhookEventsConsumer),
]
