import hashlib
import json
import os
from importlib import import_module

from channels import Group
from constance import config
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from core.packs import PACK_LOSE, PACK_WIN


class Server(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    player_limit = models.IntegerField(blank=True, null=True)
    players_online = models.PositiveIntegerField(default=0)
    auth_token = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def message_all(message):
        for server in Server.objects.all():
            server.message(message)

    def message(self, message):
        Group('server-%d' % self.id).send({"text": json.dumps(message)})

    def set_player_limit(self, limit):
        pass

    def pause(self, unpause=False):
        pass


@receiver(post_save, sender=Server)
def server_generate_auth_token(sender, instance, created, **kwargs):
    if instance.auth_token is None or instance.auth_token == '':
        instance.auth_token = hashlib.sha1(os.urandom(128)).hexdigest()
        instance.save()


class Player(models.Model):
    ingame_name = models.CharField(max_length=255)
    on_server = models.ForeignKey(Server, blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    times_joined = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.ingame_name

    def ban(self, reason):
        pass


class Game(models.Model):
    SCENARIO_CONSUMPTION_CHALLENGE = 'consumption'
    SCENARIO_PRODUCTION_CHALLENGE = 'production'
    SCENARIO_ROCKETRACE = 'rocket'

    SCENARIO_CHOICES = (
        (SCENARIO_CONSUMPTION_CHALLENGE, 'Consumption Challenge'),
        (SCENARIO_PRODUCTION_CHALLENGE, 'Production Challenge'),
        (SCENARIO_ROCKETRACE, 'Rocket Race'),
    )

    name = models.CharField(max_length=255)
    game_start = models.DateTimeField()
    game_end = models.DateTimeField(blank=True, null=True)
    game_over = models.BooleanField()
    scenario = models.CharField(max_length=32,
                                choices=SCENARIO_CHOICES,
                                default=SCENARIO_ROCKETRACE)

    scenario_data = models.TextField(
        blank=True, null=True,
        help_text="(Optional) JSON blob to configure scenario")

    class DoesNotExistException(Exception):
        pass

    def __str__(self):
        return "Game <{:d}> {:s}".format(self.pk, self.name)

    @classmethod
    def get_active(cls):
        return cls.objects.get(id=config.ACTIVE_GAME)

    def get_scenario(self):
        try:
            return import_module('scenarios.%s' % self.scenario)
        except ImportError:
            raise self.DoesNotExistException("Scenario does not exist")

    def finish(self, winner):
        """Finalize this game and notify the servers.

        Args:
            winner: A server object
        """

        if self.game_over:
            return False

        for p in Player.objects.all():
            p.on_server = None
            p.save()

        for s in Server.objects.all():
            s.players_online = 0
            s.save()

        self.game_end = timezone.now()
        self.game_over = True
        self.save()

        for server in Server.objects.all():
            if server == winner:
                server.message(PACK_WIN)
            else:
                server.message(PACK_LOSE)

        return True

    def broadcast(self, namespace, data):
        """Send a message to all our servers

        Args:
            namespace: A string describing a namespace.
            data: The data you want to send.
        """
        pack = {'namespace': namespace, 'data': data}
        for server in Server.objects.all():
            server.message(pack)

    def get_scenario_data(self):
        return json.loads(self.scenario_data)


class Event(models.Model):
    EVENT_PLAYER_JOINED = 'player_joined'
    EVENT_PLAYER_LEFT = 'player_left'
    EVENT_ROCKET_LAUNCHED = 'rocket_launched'

    EVENT_CHOICES = (
        (EVENT_PLAYER_JOINED, 'Player Joined'),
        (EVENT_PLAYER_LEFT, 'Player Left'),
        (EVENT_ROCKET_LAUNCHED, 'Rocket Launched'),
    )

    server = models.ForeignKey(Server)
    time = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=255, choices=EVENT_CHOICES)
    data = models.TextField()
    game = models.ForeignKey(Game)

    def __str__(self):
        return "[{:s}] <{:s}> {:s}".format(
            self.time.strftime('%d/%m %H:%M:%S'),
            self.server.name,
            self.get_event_display()
        )


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, created, **kwargs):
    if created:
        # Update Player list
        if instance.event == instance.EVENT_PLAYER_JOINED:
            data = json.loads(instance.data)
            p, created = Player.objects.get_or_create(
                ingame_name=data['playername'])

            p.on_server = instance.server
            p.last_seen = timezone.now()
            p.times_joined += 1
            p.save()

        elif instance.event == instance.EVENT_PLAYER_LEFT:
            data = json.loads(instance.data)
            p, created = Player.objects.get_or_create(
                ingame_name=data['playername'])

            p.on_server = None
            p.last_seen = timezone.now()
            p.save()

        # Send to scenario
        scenario = Game.get_active().get_scenario()
        scenario.event_received(instance)


class BaseStat(models.Model):
    ws_namespace = "basestat"

    server = models.ForeignKey(Server)
    time = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=100)
    value = models.IntegerField()
    game = models.ForeignKey(Game)

    class Meta:
        abstract = True

    def __str__(self):
        return "[{:s}] <{:s}> {:s}: {:d}".format(
            self.time.strftime('%d/%m %H:%M:%S'),
            self.server.name,
            self.key,
            self.value
        )

    def broadcast(self, group=None, request=None):
        """Broadcast this stat over websocket.

        Args:
            group: the name of the channels group
            request: the original message (this uses message.reply_channel)
        """
        data = json.dumps({
            'namespace': self.ws_namespace,
            'server': self.server.name,
            'type': self.key,
            'data': {
                'value': self.value,
                'timestamp': int(self.time.strftime('%s'))
            }
        })

        if group:
            Group(group).send({'text': data})
        if request:
            request.reply_channel.send({'text': data})


class ProductionStat(BaseStat):
    ws_namespace = 'production'


class ConsumptionStat(BaseStat):
    ws_namespace = 'consumption'


@receiver(post_save, sender=ProductionStat)
def productionstat_postsave(sender, instance, created, **kwargs):
    scenario = Game.get_active().get_scenario()
    scenario.productionstat_received(instance)

    instance.broadcast(group='public')


@receiver(post_save, sender=ConsumptionStat)
def consumptionstat_postsave(sender, instance, created, **kwargs):
    scenario = Game.get_active().get_scenario()
    scenario.consumptionstat_received(instance)

    instance.broadcast(group='public')


class ScenarioData(models.Model):
    """ For saving scenario data """
    server = models.ForeignKey(Server, blank=True, null=True)
    key = models.CharField(max_length=255)
    value = models.TextField()
    game = models.ForeignKey(Game)

    def __str__(self):
        try:
            return "<{:s}> {:s} : {:s}".format(
                self.server.name,
                self.key,
                self.value
            )
        except AttributeError:
            return "<none> {:s} : {:s}".format(
                self.key,
                self.value
            )
