from core.models import (ConsumptionStat, Event, Player, ProductionStat,
                         ScenarioData, Server)
from django.contrib import admin

admin.site.register(ConsumptionStat)
admin.site.register(Event)
admin.site.register(Player)
admin.site.register(ProductionStat)
admin.site.register(Server)
admin.site.register(ScenarioData)
