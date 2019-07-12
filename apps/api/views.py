from typing import Any, Dict

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import WebhookEventSerializer


class CreateWebhookEvent(generics.CreateAPIView):
    serializer_class = WebhookEventSerializer

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
            return Response('Successfuly handled the webhook event', status=status.HTTP_201_CREATED)
        return Response('Bad data', status=status.HTTP_400_BAD_REQUEST)
