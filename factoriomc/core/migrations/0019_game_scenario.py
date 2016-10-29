# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20161009_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='scenario',
            field=models.CharField(max_length=32, default='rocket', choices=[('consumption', 'Consumption Challenge'), ('production', 'Production Challenge'), ('rocket', 'Rocket Race')]),
        ),
    ]
