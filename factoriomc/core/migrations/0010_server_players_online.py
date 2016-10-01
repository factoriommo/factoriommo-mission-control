# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_scenariodata'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='players_online',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
