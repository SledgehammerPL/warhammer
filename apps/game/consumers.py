import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger('error_logger')


def _chat_group_name(raw_value):
    # Channels allows only ASCII alnum, hyphen, underscore and dot.
    ascii_value = str(raw_value or "").encode("ascii", "ignore").decode("ascii")
    safe_value = re.sub(r"[^A-Za-z0-9_.-]+", "_", ascii_value).strip("_.-")
    if not safe_value:  # Ensure safe_value is not empty
        safe_value = "anonymous"
    return f"chat_{safe_value}"[:99]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.leader_name = self.scope['url_route']['kwargs']['leader_name']
        self.leader_group_name = _chat_group_name(self.leader_name)

        # Join leader group
        await self.channel_layer.group_add(
            self.leader_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave leader group
        await self.channel_layer.group_discard(
            self.leader_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to leader group
        await self.channel_layer.group_send(
            self.leader_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from leader group
    async def redirect(self, event):
        redirect = event['redirect']
        logger.error('jestem w redirekcie')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'redirect': redirect
        }))

    # Receive message from leader group
    async def chat_message(self, event):
        logger.error('jestem w CHAT_mesaGE')
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
