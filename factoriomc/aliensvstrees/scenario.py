from core.models import Server, ConsumptionStat


class Scenario(object):

    def tick(self):
        # Send Production stats
        servers = Server.objects.all()

        data_list = { }

        for server in servers:
            try:
                pack1 = ConsumptionStat.objects.filter(server=server.id) \
                    .filter(key='science-pack-1').order_by('-id')[0].value
            except IndexError:
                pack1 = 0
            try:
                pack2 = ConsumptionStat.objects.filter(server=server.id) \
                    .filter(key='science-pack-2').order_by('-id')[0].value
            except IndexError:
                pack2 = 0
            try:
                pack3 = ConsumptionStat.objects.filter(server=server.id) \
                    .filter(key='science-pack-3').order_by('-id')[0].value
            except IndexError:
                pack3 = 0
            try:
                pack4 = ConsumptionStat.objects.filter(server=server.id) \
                    .filter(key='alien-science-pack').order_by('-id')[0].value
            except IndexError:
                pack4 = 0

            data_list[server.pk] = {
                'science-pack-1': pack1,
                'science-pack-2': pack2,
                'science-pack-3': pack3,
                'alien-science-pack': pack4,
                'players-online': '0',
            }

        pack = {'namespace': 'scores', 'data': data_list}
        for server in servers:
            server.message(pack)


def event_received(event):
    if event.event == event.EVENT_PLAYER_JOINED:
        return
    elif event.event == event.EVENT_PLAYER_LEFT:
        return
    elif event.event == event.EVENT_ROCKET_LAUNCHED:
        pack = {"namespace": "chat", "data":
                {"msg": "Uh-oh, the %s server just launched a rocket.." % event.server.name}}

        for server in Server.objects.all():
            if server != event.server:
                server.message(pack)
