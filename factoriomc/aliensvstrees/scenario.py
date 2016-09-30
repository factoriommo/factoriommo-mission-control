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
