from django.views.generic import TemplateView


class WebhooksView(TemplateView):
    template_name = 'webhooks.html'
