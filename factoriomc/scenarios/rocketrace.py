from core.models import ConsumptionStat, ScenarioData, Server, Game
from django.conf import settings


PACK_WIN = {"namespace": "victory", "data": {"winner": True}}
PACK_LOSE = {"namespace": "victory", "data": {"winner": False}}

TARGET_PACK_1 = 8000
TARGET_PACK_2 = 8000
TARGET_PACK_3 = 2000
TARGET_PACK_4 = 250


PACK_DICT = {
    'science-pack-1': 'Red science',
    'science-pack-2': 'Green science',
    'science-pack-3': 'Blue science',
    'alien-science-pack': 'Alien science',
    'rocket-progress': 'Rocket progress'
}


def update_stats():
    # Send Production stats
    servers = Server.objects.all()
    active_game = Game.get_active()

    data_list = {}

    for server in servers:
        data_list[server.pk] = {'players-online': str(server.players_online)}

        for key in PACK_DICT:
            try:
                data_list[server.pk][key] = ConsumptionStat.objects \
                    .filter(server=server.id) \
                    .filter(key=key) \
                    .filter(game=active_game) \
                    .order_by('-id')[0].value
            except IndexError:
                data_list[server.pk][key] = 0

    pack = {'namespace': 'scores', 'data': data_list}
    for server in servers:
        server.message(pack)

    lead_table = {}
    # Update lead tables
    for key in PACK_DICT:
        try:
            lead_table[key] = ScenarioData.objects.get(key='leader-%s' % key,
                                                       game=active_game)
        except ScenarioData.DoesNotExist:
            lead_table[key] = ScenarioData.objects.create(
                key='leader-%s' % key,
                value=0,
                game=active_game)

    new_leaders = {}
    for key in PACK_DICT:
        # Find highest server for key
        highest = 0
        highest_server = None
        for server in servers:
            if int(data_list[server.pk][key]) > int(lead_table[key].value):
                if int(data_list[server.pk][key]) > highest:
                    highest = data_list[server.pk][key]
                    highest_server = server

        if highest_server is not None:
            new_leaders[key] = highest_server

    for key in PACK_DICT:
        if key not in new_leaders:
            continue

        if lead_table[key].server is None or \
                new_leaders[key].pk != lead_table[key].server.pk:
            # Save new leader

            for server in servers:
                if server is new_leaders[key]:
                    pack = {
                        "namespace": "chat",
                        "data": {
                            "msg": "You have taken the lead in {:s}"
                            .format(PACK_DICT[key])}}

                    server.message(pack)
                else:
                    pack = {
                        "namespace": "chat",
                        "data": {
                            "msg": "{:s} have taken the lead in {:s}"
                            .format(new_leaders[key].name, PACK_DICT[key])}}

                    server.message(pack)

        lead_table[key].server = new_leaders[key]
        lead_table[key].value = data_list[new_leaders[key].pk][key]
        lead_table[key].save()


def event_received(event):
    if event.event == event.EVENT_PLAYER_JOINED:
        update_stats()
    elif event.event == event.EVENT_PLAYER_LEFT:
        update_stats()
    elif event.event == event.EVENT_ROCKET_LAUNCHED:
        # See if we have a winner
        servers = Server.objects.all()
        game = Game.objects.get(pk=settings.ACTIVE_GAME)

        if not game.game_over:
            game.game_over = True
            game.save()
            for server in servers:
                if server == event.server:  # This is the winning server
                    server.message(PACK_WIN)
                else:
                    server.message(PACK_LOSE)  # This is the losing server


def consumptionstat_received(stat):
    update_stats()


def productionstat_received(stat):
    pass
