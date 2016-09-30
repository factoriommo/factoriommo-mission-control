import json

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from core.models import ConsumptionStat, Event, ProductionStat, Server
from django.http import HttpResponse

PACK_AUTH_OK = {  # Auth succeeds
    "namespace": "auth",
    "data": {
        "success": True
    }
}

PACK_AUTH_FAIL = {  # Auth fails
    "namespace": "auth",
    "data": {
        "success": False
    }
}

PACK_NO_AUTH = {  # Sending packages without being authed
    "namespace": "auth",
    "data": {
        "success": False,
        "msg": "Please authenticate first"
    }
}

PACK_NO_SERVER = {  # Connected to a websocket server endpoint that doesn't exist
    "namespace": "global",
    "data": {
        "success": False,
        "msg": "This endpoint does not exist."
    }
}


def ok_pack(namespace):
    return {
        'text': json.dumps({
            "namespace": namespace,
            "data": {
                "success": True
            }
        })
    }


def fail_pack(namespace, msg):
    return {
        'text': json.dumps({
            "namespace": namespace,
            "data": {
                "success": True,
                "msg": msg
            }
        })
    }


@channel_session
def server_connected(message, pk=None):
    print("New connection on channel server %s" % (pk,))


@channel_session
def server_message(message, pk=None):
    raw_pack = json.loads(message.content['text'])
    namespace, msg = raw_pack['namespace'], raw_pack['data']
    try:
        server = Server.objects.get(pk=pk)
    except Server.DoesNotExist:
        print("Connection to unknown server..")
        message.reply_channel.send({'text': json.dumps(PACK_NO_SERVER)})
        return

    if 'authed' not in message.channel_session:
        if namespace == 'auth':
            print("Authenticating...", end='')
            if server.auth_token == msg['token']:
                message.channel_session['authed'] = True
                response = PACK_AUTH_OK
                print("Succes")
            else:
                response = PACK_AUTH_FAIL
                print("Fail")

            message.reply_channel.send({'text': json.dumps(response)})
        else:
            message.reply_channel.send({'text': json.dumps(PACK_NO_AUTH)})
        return

    if namespace == 'auth':  # Already Authed, Defend against authloops
        message.reply_channel.send({'text': json.dumps(PACK_AUTH_OK)})

    if namespace == 'production':
        try:
            if int(msg['data']) < 0:
                raise ValueError
        except ValueError:
                message.reply_channel.send(fail_pack(namespace, "Data has to be an int bigger than 0"))
                return

        try:
            ProductionStat.objects.create(
                server = server,
                key = msg['type'],
                value = msg['data']
            )
            message.reply_channel.send(ok_pack(namespace))
        except:
            message.reply_channel.send(fail_pack(namespace, "Unknown error occured"))
            raise
        return

    if namespace == 'consumption':
        try:
            if int(msg['data']) < 0:
                raise ValueError
        except ValueError:
                message.reply_channel.send(fail_pack(namespace, "Data has to be an int bigger than 0"))
                return

        try:
            ConsumptionStat.objects.create(
                server = server,
                key = msg['type'],
                value = msg['data']
            )
            message.reply_channel.send(ok_pack(namespace))
        except:
            message.reply_channel.send(fail_pack(namespace, "Unknown error occured"))
            raise
        return

    if namespace == 'event':
        try:
            Event.objects.create(
                server = server,
                event = msg['type'],
                data = json.dumps(msg['data'])
            )
            message.reply_channel.send(ok_pack(namespace))
        except json.decoder.JSONDecodeError:
            message.reply_channel.send(fail_pack(namespace, "Please send JSON data as data"))
        return

    print ("Unknown msg: ", namespace, msg)


@channel_session
def server_disconnected(message, pk=None):
    print("Connection lost on channel server %s" % (pk,))
    # Group("broadcast-%s-%s" % (endpoint, pk)).discard(message.reply_channel)
