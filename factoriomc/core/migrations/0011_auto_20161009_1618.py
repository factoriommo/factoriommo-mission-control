# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_server_players_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='server',
            name='slug',
        ),
    ]
