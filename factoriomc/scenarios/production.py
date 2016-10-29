"""
Example Scenario data (On the Game object):

{"targets": [
    {"id": "productivity-module-3",
     "name": "Productivity",
     "target": 100
     },
     {"id": "effectivity-module-3",
      "name": "Effectivity",
      "target": 50
     },
     {"id": "speed-module-3",
      "name": "Speed",
      "target": 10
      }]
}


"""
from core.models import ProductionStat, Server, Game, ScenarioData
from constance import config


def event_received(event):
    if event.event == event.EVENT_PLAYER_JOINED:
        update_stats()
    elif event.event == event.EVENT_PLAYER_LEFT:
        update_stats()
    elif event.event == event.EVENT_ROCKET_LAUNCHED:
        pack = {
            "namespace": "chat",
            "data": {
                "msg": "Uh-oh, the {:s} server just launched a rocket.."
                .format(event.server.name)}}

        for server in Server.objects.all():
            if server != event.server:
                server.message(pack)


def consumptionstat_received(stat):
    pass


def productionstat_received(stat):
    update_stats()


def update_stats():
    game = Game.objects.get(pk=config.ACTIVE_GAME)
    servers = Server.objects.all()
    winner = None

    stats = calculate_production(game, servers)
    game.broadcast('scores', stats)

    if not game.game_over:
        calculate_leaders(game, servers, stats)
        winner = check_winner(game, servers, stats)

    if winner and not game.game_over:
        game.finish(winner)


def calculate_production(game, servers):
    """Broadcast the consumption stats to all servers

    Args:
        game: A game object.
        servers: A QuerySet with servers
    """
    data = {}

    for server in servers:
        data[server.pk] = {'players-online': str(server.players_online)}

        targets = game.get_scenario_data()['targets']
        for key in targets:
            try:
                data[server.pk][key['id']] = ProductionStat.objects \
                    .filter(server=server.id) \
                    .filter(key=key['id']) \
                    .filter(game_id=config.ACTIVE_GAME) \
                    .order_by('-id')[0].value
            except IndexError:
                data[server.pk][key['id']] = 0

    return data


def calculate_leaders(game, servers, stats):
    """Calculate the leaders

    Args:
        game: A game object.
        servers: A QuerySet with servers
        stats: The output from calculate_production
    """
    lead_table = {}

    targets = game.get_scenario_data()['targets']

    # Initialise lead_table, create empty entries in db if not found.
    for key in targets:
        try:
            lead_table[key['id']] = ScenarioData.objects.get(
                key='leader-%s' % key['id'],
                game_id=config.ACTIVE_GAME)

        except ScenarioData.DoesNotExist:
            lead_table[key['id']] = ScenarioData.objects.create(
                key='leader-%s' % key['id'],
                value=0,
                game_id=config.ACTIVE_GAME)

    # Build a table with all new leaders
    new_leaders = {}
    for key in targets:
        highest = 0
        highest_server = None
        for server in servers:
            if int(stats[server.pk][key['id']]) > int(lead_table[key['id']].value):
                if int(stats[server.pk][key['id']]) > highest:
                    highest = stats[server.pk][key['id']]
                    highest_server = server

        if highest_server is not None:
            new_leaders[key['id']] = highest_server

    # Compare current and new leaders, notify servers on change
    for key in targets:
        if key['id'] not in new_leaders:
            continue  # No change

        if lead_table[key['id']].server is None or \
                new_leaders[key['id']].pk != lead_table[key['id']].server.pk:
            # A new leader appeared

            for server in servers:
                if server is new_leaders[key['id']]:
                    # Notify the server that has taken the lead
                    pack = {
                        "namespace": "chat",
                        "data": {
                            "msg": "You have taken the lead in {:s}, well done!"
                            .format(key['name'])}}

                    server.message(pack)
                else:
                    # Notify the other servers that they should try harder.
                    pack = {
                        "namespace": "chat",
                        "data": {
                            "msg": "{:s} have taken the lead in {:s}. Work harder!"
                            .format(new_leaders[key['id']].name, key['name'])}}
                    server.message(pack)

        lead_table[key['id']].server = new_leaders[key['id']]
        lead_table[key['id']].value = stats[new_leaders[key['id']].pk][key['id']]
        lead_table[key['id']].save()

    return lead_table


def check_winner(game, servers, stats):
    """See if we have a winner

    Args:
        game: A game object.
        servers: A QuerySet with servers
        stats: The output from calculate_production

    Returns:
        Server if winner
    """

    # stats[server.pk][target['id']] = int

    data = game.get_scenario_data()

    for server in servers:
        winning = True
        for target in data['targets']:
            if stats[server.pk][target['id']] < target['target']:
                winning = False
        if winning:
            return server
