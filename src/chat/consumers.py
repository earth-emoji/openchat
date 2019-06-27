import asyncio
import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.shortcuts import redirect, reverse

from .models import Room, Message
from accounts.models import UserProfile


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connect", event)

        user = self.scope['user']
        if user.is_authenticated:
            await self.send({
                'type':'websocket.accept',
            })

            # get user and room
            self.profile = UserProfile.objects.get(user=user)
            
            self.room_url = self.scope['url_route']['kwargs']['url']

            self.room = Room.objects.get(url=self.room_url)
            
            await self.channel_layer.group_add(
                    self.room_url,
                    self.channel_name
            )

            await self.send({
                "type": "websocket.send",
                "text": self.room_url
            })


    async def websocket_receive(self, event):
        print("receive", event)
        text = event.get('text', None)

        if text is not None:
            loaded_data = json.loads(text)
            msg = loaded_data.get('message')
            user = self.scope['user']

            if user.is_authenticated:
                jsonResponse = {
                    'message': msg,
                    'username': self.profile.user.username
                }

                # save to database
                await self.create_message(msg)

                # broadcast data back to client
                await self.channel_layer.group_send(
                    self.room_url,
                    {
                        "type": "chat_message",
                        "text": json.dumps(jsonResponse)
                    }
                )

    async def chat_message(self, event):
        # send the actual message
        print("message", event)
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnect", event)

    @database_sync_to_async
    def create_message(self, msg):
        return Message.objects.create(sender=self.profile, message=msg, room=self.room)