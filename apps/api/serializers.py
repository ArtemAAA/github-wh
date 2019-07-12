from logging import getLogger

from rest_framework import serializers

from apps.webhooks.models import WebhookEvent


logger = getLogger(__name__)


class WebhookEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebhookEvent
        fields = '__all__'

    def to_internal_value(self, data):
        event_name = data.pop('event_name')
        action = data.pop('action', '')

        repository = data.pop('repository', '')
        if isinstance(repository, dict):
            repository = repository.get('html_url', '')

        sender = data.pop('sender', '')
        if isinstance(sender, dict):
            sender = sender.get('html_url', '')

        if not any((repository, sender)):
            logger.warning(
                'WebhookEventSerializer.to_internal_value: not enough data - '
                f'repository={repository}, sender={sender} | data={data}'
            )

        event_data = data.pop(event_name, None)
        if event_data is None:
            event_data = data.copy()
            # remove model fields from the data
            for field_name in self.fields.keys():
                event_data.pop(field_name, None)

        result = {
            'action': action,
            'event_data': event_data,
            'event_name': event_name,
            'repository': repository,
            'sender': sender,
        }

        return result
