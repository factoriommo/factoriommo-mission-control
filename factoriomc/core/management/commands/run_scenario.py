from time import sleep

from django.core.management.base import BaseCommand
from django.db import reset_queries
from django.conf import settings


class Command(BaseCommand):
    help = 'Run scenario one'

    def handle(self, *args, **options):
        running=True

        self.stdout.write("Starting scenario %s.." % settings.SCENARIO)
        scenario_module = __import__('%s.scenario' % settings.SCENARIO)
        scenario = scenario_module.scenario.Scenario()
        while running:
            reset_queries()
            sleep(1)
            print(".")
            try:
                scenario.tick()
            except KeyboardInterrupt:
                self.stdout.write("Stopping..")
                running=False
                continue
