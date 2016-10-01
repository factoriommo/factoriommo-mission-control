from core.models import Server, ConsumptionStat

PACK_WIN = {"namespace": "victory", "data": { "winner": True }}
PACK_LOSE = {"namespace": "victory", "data": { "winner": False }}

TARGET_PACK_1 = 8000
TARGET_PACK_2 = 8000
TARGET_PACK_3 = 2000
TARGET_PACK_4 = 250

class Scenario(object):

    def tick(self):
        pass


def update_stats():
    # Send Production stats
    servers = Server.objects.all()

    data_list = { }

    for server in servers:
        data_list[server.pk] = {'players-online': str(server.player_set.count())}

        for key in ['science-pack-1', 'science-pack-2', 'science-pack-3', 'alien-science-pack']:
            try:
                data_list[server.pk][key] = ConsumptionStat.objects.filter(server=server.id) \
                    .filter(key=key).order_by('-id')[0].value
            except IndexError:
                data_list[server.pk][key] = 0

    pack = {'namespace': 'scores', 'data': data_list}
    for server in servers:
        server.message(pack)

    winner = None
    # See if we have a winner
    for server in servers:
        if data_list[server.pk]['science-pack-1'] >= TARGET_PACK_1 and \
                data_list[server.pk]['science-pack-2'] >= TARGET_PACK_2 and \
                data_list[server.pk]['science-pack-3'] >= TARGET_PACK_3 and \
                data_list[server.pk]['alien-science-pack'] >= TARGET_PACK_4:
            winner = server
            break

    if winner:
        for server in servers:
            if server == winner:
                server.message(PACK_WIN)
            else:
                server.message(PACK_LOSE)


def event_received(event):
    if event.event == event.EVENT_PLAYER_JOINED:
        update_stats()
    elif event.event == event.EVENT_PLAYER_LEFT:
        update_stats()
    elif event.event == event.EVENT_ROCKET_LAUNCHED:
        pack = {"namespace": "chat", "data":
                {"msg": "Uh-oh, the %s server just launched a rocket.." % event.server.name}}

        for server in Server.objects.all():
            if server != event.server:
                server.message(pack)


def consumptionstat_received(stat):
    update_stats()


def productionstat_received(stat):
    pass
