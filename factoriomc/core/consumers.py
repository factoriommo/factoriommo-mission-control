import json

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from core.models import Server
from django.http import HttpResponse

PACK_AUTH_OK = {
    "namespace": "auth",
    "data": {
        "success": True
    }
}

PACK_AUTH_FAIL = {
    "namespace": "auth",
    "data": {
        "success": False
    }
}

PACK_NO_AUTH = {
    "namespace": "auth",
    "data": {
        "success": False,
        "msg": "Please authenticate first"
    }
}


@channel_session
def server_connected(message, pk=None):
    print("New connection on channel server %s" % (pk,))


@channel_session
def server_message(message, pk=None):
    raw_pack = json.loads(message.content['text'])
    namespace, msg = raw_pack['namespace'], raw_pack['data']
    if 'authed' not in message.channel_session:
        if namespace == 'auth':
            print("Authenticating...", end='')
            try:
                s = Server.objects.get(pk=pk, auth_token=msg['token'])
                response = PACK_AUTH_OK
                message.channel_session['authed'] = True
                print("Succes")
            except Server.DoesNotExist:
                response = PACK_AUTH_FAIL
                print("Fail")

            message.reply_channel.send({'text': json.dumps(response)})
            return
        else:
            message.reply_channel.send({'text': json.dumps(PACK_NO_AUTH)})

    else:
        print ("Unknown msg: ", namespace, msg)
    #message.channel_session['room']


@channel_session
def server_disconnected(message, pk=None):
    print("Connection lost on channel server %s" % (pk,))
    # Group("broadcast-%s-%s" % (endpoint, pk)).discard(message.reply_channel)
