import json

from channels.generic.websocket import AsyncWebsocketConsumer

from github_wh.settings import CHANNEL_NAME


class WebhookEventsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.channel = CHANNEL_NAME
        await self.channel_layer.group_add(self.channel, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.channel, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_event(self, event):
        await self.send(text_data=json.dumps(event["data"]))
