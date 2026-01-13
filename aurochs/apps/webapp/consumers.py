import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.auth import get_user
import channels.layers
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from api.events import event_handlers


# Code from inkshop to handle websocket k-v sync.


class EventConsumer(WebsocketConsumer):
    def connect(self):
        self.user_ox_id = self.scope["url_route"]["kwargs"]["user_ox_id"]
        self.room_group_name = "u-%s" % (self.user_ox_id,)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        self.user = async_to_sync(get_user)(self.scope)
        data = json.loads(text_data)

        # print(data)
        # print(self.user)
        data["_server_timestamp"] = timezone.now().timestamp() * 1000
        if data["event_type"] in event_handlers:
            ret = event_handlers[data["event_type"]]().handle(
                self,
                data,
            )
        # print(ret)
        # print("self.channel_layer.group_send")
        # print(self.channel_layer.group_send)

        if not self.user.is_anonymous:
            # if "alive" in data and data["alive"]:
            #     return

            # p = None
            # try:
            #     p = Person.objects.get(hashid=self.user_ox_id)
            # except:
            #     import traceback

            #     traceback.print_exc()
            #     pass

            # if p and p == self.user:
            #     p.data = json.dumps(data)
            #     p.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "data_update", "data": ret}
            )

            return

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "unauthorized",
                "data": {"consumerguid": data.get("consumerguid", "")},
            },
        )

    # Receive message from room group
    def data_update(self, event):
        data = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": "data_update", "data": data}))

    def oxgpt_event(self, event):
        data = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": "oxgpt_event", "data": data}))

    def export_event(self, event):
        data = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": "export_event", "data": data}))

    # Receive message from room group
    def unauthorized(self, event):
        data = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": "unauthorized", "data": data}))
