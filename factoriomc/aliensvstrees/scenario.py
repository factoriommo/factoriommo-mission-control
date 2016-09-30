from core.models import Server, ConsumptionStat


class Scenario(object):

    def tick(self):
        # Send Production stats
        servers = Server.objects.all()

        data_list = { }

        for server in servers:
            data_list[server.pk] = {'players-online': '0'}

            for key in ['science-pack-1', 'science-pack-2', 'science-pack-3', 'alien-science-pack']:
                try:
                    data_list[server.pk][key] = ConsumptionStat.objects.filter(server=server.id) \
                        .filter(key=key).order_by('-id')[0].value
                except IndexError:
                    data_list[server.pk][key] = 0

        pack = {'namespace': 'scores', 'data': data_list}
        for server in servers:
            server.message(pack)


def event_received(event):
    if event.event == event.EVENT_PLAYER_JOINED:
        print('Scenario player joined')
        return
    elif event.event == event.EVENT_PLAYER_LEFT:
        print('Scenario player left')
        return
    elif event.event == event.EVENT_ROCKET_LAUNCHED:
        pack = {"namespace": "chat", "data":
                {"msg": "Uh-oh, the %s server just launched a rocket.." % event.server.name}}

        for server in Server.objects.all():
            if server != event.server:
                server.message(pack)
