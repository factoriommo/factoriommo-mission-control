from time import sleep

from core.models import Server, ConsumptionStat
from django.core.management.base import BaseCommand
from django.db import reset_queries

WAIT_TIME = 2


class Command(BaseCommand):
    help = 'Run scenario one'

    def handle(self, *args, **options):
        running=True

        self.stdout.write("Starting scenario one..")
        while running:
            reset_queries()
            try:
                sleep(WAIT_TIME)
                print(".")
                # Send Production stats
                servers = Server.objects.all()

                data_list = { }

                for server in servers:
                    try:
                        pack1 = ConsumptionStat.objects.filter(server=1).filter(key='science-pack-1').order_by('-id')[0]
                    except IndexError:
                        pack1 = 0
                    try:
                        pack2 = ConsumptionStat.objects.filter(server=1).filter(key='science-pack-2').order_by('-id')[0]
                    except IndexError:
                        pack2 = 0
                    try:
                        pack3 = ConsumptionStat.objects.filter(server=1).filter(key='science-pack-3').order_by('-id')[0]
                    except IndexError:
                        pack3 = 0
                    try:
                        pack4 = ConsumptionStat.objects.filter(server=1).filter(key='alien-science-pack').order_by('-id')[0]
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
            except KeyboardInterrupt:
                self.stdout.write("Stopping..")
                running=False
                continue
