from django.db import models


class WebhookEvent(models.Model):
    action = models.CharField(max_length=30)
    event_name = models.CharField(max_length=50)
    event_data = models.TextField()  # TODO: use JSONField instead?
    repository = models.URLField(max_length=200)
    sender = models.URLField(max_length=200)

    def __str__(self):
        return f'<WebhookEvent: {self.event_name} - {self.repository[:20]}>'
