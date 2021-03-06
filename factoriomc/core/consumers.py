from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session

from core.models import ConsumptionStat, Event, ProductionStat, Server, Game
from constance import config

import json


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

PACK_NO_SERVER = {  # Server not found package
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
                "success": False,
                "msg": msg
            }
        })
    }


@channel_session
def server_connected(message, pk=None):
    print("New connection on channel server %s" % (pk,))


@channel_session
def server_disconnected(message, pk=None):
    Group('server-%s' % pk).discard(message.reply_channel)
    print("Connection lost on channel server %s" % (pk,))
    # Group("broadcast-%s-%s" % (endpoint, pk)).discard(message.reply_channel)


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
                Group('server-%d' % server.id).add(message.reply_channel)
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
                message.reply_channel.send(
                    fail_pack(namespace, "Data has to be an int > than 0"))
                return

        try:
            ProductionStat.objects.create(
                server=server,
                key=msg['type'],
                value=msg['data'],
                game_id=config.ACTIVE_GAME
            )
            message.reply_channel.send(ok_pack(namespace))
        except:
            message.reply_channel.send(
                fail_pack(namespace, "Unknown error occured"))
            raise
        return

    if namespace == 'consumption':
        try:
            if int(msg['data']) < 0:
                raise ValueError
        except ValueError:
                message.reply_channel.send(
                    fail_pack(namespace, "Data has to be an int > than 0"))
                return

        try:
            ConsumptionStat.objects.create(
                server=server,
                key=msg['type'],
                value=msg['data'],
                game_id=config.ACTIVE_GAME
            )
            message.reply_channel.send(ok_pack(namespace))
        except:
            message.reply_channel.send(
                fail_pack(namespace, "Unknown error occured"))
            raise
        return

    if namespace == 'event':
        Event.objects.create(
            server=server,
            event=msg['type'],
            data=json.dumps(msg['data']),
            game_id=config.ACTIVE_GAME
        )
        message.reply_channel.send(ok_pack(namespace))
        return

    if namespace == 'updatecounter':
        try:
            if msg['type'] == "player-online-count":
                server.players_online = int(msg['data'])
                server.save()
                message.reply_channel.send(ok_pack(namespace))
            elif msg['type'] == "rocket-progress":
                ConsumptionStat.objects.create(
                    server=server,
                    key=msg['type'],
                    value=msg['data'],
                    game_id=config.ACTIVE_GAME
                )
                message.reply_channel.send(ok_pack(namespace))
        except:
            message.reply_channel.send(
                fail_pack(namespace, "Unknown error occured"))

        return

    print("Unknown msg: ", namespace, msg)


@channel_session_user_from_http
def admin_connected(message):
    print("New connection on admin panel from %s" % message.user)


@channel_session_user
def admin_disconnected(message):
    print("Connection lost on admin panel from %s" % message.user)


@channel_session_user
def admin_message(message, pk=None):
    if not message.user.is_staff:
        message.reply_channel.send(fail_pack('global', "Nope."))

    raw_pack = json.loads(message.content['text'])
    namespace, msg = raw_pack['namespace'], raw_pack['data']

    if namespace == 'chat':
        if msg['target'] == 'all':
            del(raw_pack['data']['target'])
            pack = json.dumps(raw_pack)
            for s in Server.objects.all():
                Group('server-%s' % s.id).send({"text": pack})
        else:
            target = msg['target']
            del(raw_pack['data']['target'])
            pack = json.dumps(raw_pack)
            try:
                Group('server-%d' % int(target)).send({"text": pack})
            except ValueError:
                message.reply_channel.send(fail_pack('chat', "Server failed."))
        return

    if namespace == 'rconcommand':
        pack = json.dumps(raw_pack)
        for server in Server.objects.all():
            try:
                Group('server-%d' % int(server.id)).send({"text": pack})
            except ValueError:
                message.reply_channel.send(fail_pack('chat', "Server failed."))
                return

        message.reply_channel.send(ok_pack(namespace))
        return

    print("Unknown admin msg: ", namespace, msg)


@channel_session_user_from_http
def public_connected(message):
    print("New connection on public channel from %s" % message.user)
    Group('public').add(message.reply_channel)

    game = Game.get_active()
    for i in game.productionstat_set.order_by('-time'):
        i.broadcast(request=message)
    for i in game.consumptionstat_set.order_by('-time'):
        i.broadcast(request=message)


@channel_session_user
def public_disconnected(message):
    print("Connection lost on public channel from %s" % message.user)
    Group('public').discard(message.reply_channel)


@channel_session_user
def public_message(message, pk=None):
    print("Dropping package on public channel: %s" % message.text)
