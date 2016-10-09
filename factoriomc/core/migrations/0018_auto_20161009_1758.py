# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20161009_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_end',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
