# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20161009_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenariodata',
            name='game',
            field=models.ForeignKey(to='core.Game', default=1),
            preserve_default=False,
        ),
    ]
