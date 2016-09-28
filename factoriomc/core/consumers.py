import json

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session


def server_connected(message, pk=None):
    print(message)

def server_message(message, pk=None):
    msg = json.loads(message.content['text'])
    print(msg)

def server_disconnected(message, pk=None):
    print(message)
    # Group("broadcast-%s-%s" % (endpoint, pk)).discard(message.reply_channel)
