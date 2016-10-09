# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from datetime import datetime


def create_first_game(apps, schema_editor):
    Game = apps.get_model("core", "Game")
    Event = apps.get_model("core", "Event")
    ConsumptionStat = apps.get_model("core", "ConsumptionStat")

    try:
        first_event = Event.objects.all().order_by('time').first()
        last_event = Event.objects.all().order_by('time').last()
    except Event.DoesNotExist:
        print("WARN: No data found. Not running data migation")
        return

    game = Game.objects.create(
        name="Aliens vs Trees",
        game_start=first_event.time,
        game_end=last_event.time
    )



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_game'),
    ]

    operations = [
        migrations.RunPython(create_first_game),
    ]
