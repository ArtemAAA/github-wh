from typing import Any, Dict

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.webhooks.models import WebhookEvent
from github_wh.settings import CHANNEL_NAME
from .serializers import WebhookEventSerializer


class WebhookEventList(generics.ListCreateAPIView):
    serializer_class = WebhookEventSerializer
    queryset = WebhookEvent.objects.all()

    skip_fields = ('csrfmiddlewaretoken', )

    def remove_skipped_fields(self, data: Dict[str, Any]):
        for field in self.skip_fields:
            data.pop(field, None)
        return data

    @method_decorator(csrf_exempt)
    def post(self, request, *arg, **kwargs):
        data = request.data.copy()
        self.remove_skipped_fields(data)

        event_name = request.META.get('HTTP_X_GITHUB_EVENT')
        if event_name is None:
            return Response('Bad data', status=status.HTTP_400_BAD_REQUEST)

        data['event_name'] = event_name

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(CHANNEL_NAME, {
                "type": "send_event",
                "data": serializer.data,
            })
            return Response('Successfuly handled the webhook event', status=status.HTTP_201_CREATED)
        return Response('Bad data', status=status.HTTP_400_BAD_REQUEST)
