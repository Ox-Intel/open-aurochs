from django.urls import re_path

from webapp import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/p/(?P<user_ox_id>[0-9A-Za-z_\-]+)/$", consumers.EventConsumer.as_asgi()
    ),
]
