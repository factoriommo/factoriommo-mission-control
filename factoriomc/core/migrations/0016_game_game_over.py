# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_scenariodata_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_over',
            field=models.BooleanField(default=True),
        ),
    ]
