from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/party/(?P<leader_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
