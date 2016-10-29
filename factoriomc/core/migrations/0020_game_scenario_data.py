# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_game_scenario'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='scenario_data',
            field=models.TextField(blank=True, help_text='(Optional) JSON blob to configure scenario', null=True),
        ),
    ]
