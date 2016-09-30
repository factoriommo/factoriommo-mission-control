# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20161001_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='times_joined',
            field=models.IntegerField(default=0),
        ),
    ]
