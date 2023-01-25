# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        user_profile_photo = "/static/final_main_app/user.png"

        try:
            user_profile_photo = self.user.appuser.images.first().thumbnail.url
        except:
            print("An exception occurred")

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = datetime.now()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'thumbnail': user_profile_photo,
                'role': self.user.appuser.role,
                'message_time_stamp': now.strftime("%d %B %H:%M")
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        user_profile_photo = event['thumbnail']
        message_time_stamp = event['message_time_stamp']
        if event['username'] == self.user.username:
            own_message = True
        else:
            own_message = False

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'thumbnail': user_profile_photo,
            'message_time_stamp': message_time_stamp,
            'own_message': own_message
        }))
