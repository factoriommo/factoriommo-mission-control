from channels.auth import channel_session_user, channel_session_user_from_http
from channels import Group
from channels.sessions import channel_session

@channel_session_user_from_http
def server_connected(message, pk=None):
	pass

@channel_session_user
def server_message(message, pk=None):
    pass

@channel_session_user
def server_disconnected(message, pk=None):
    # Group("broadcast-%s-%s" % (endpoint, pk)).discard(message.reply_channel)
    pass
