# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20161009_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumptionstat',
            name='game',
            field=models.ForeignKey(to='core.Game', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(to='core.Game', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productionstat',
            name='game',
            field=models.ForeignKey(to='core.Game', default=1),
            preserve_default=False,
        ),
    ]
