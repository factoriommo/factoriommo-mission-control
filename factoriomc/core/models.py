import hashlib
import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Server(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=32)
    player_limit = models.IntegerField(blank=True, null=True)
    auth_token = models.CharField(max_length=40, blank=True, null=True)

    def message(self, message):
        pass

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
    last_seen = models.DateTimeField()
    times_joined = models.IntegerField()

    def ban(self, reason):
        pass


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


class BaseStat(models.Model):
    server = models.ForeignKey(Server)
    time = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        abstract = True


class ProductionStat(BaseStat):
    pass


class ConsumptionStat(BaseStat):
    pass
