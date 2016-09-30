# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20160929_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='slug',
            field=models.SlugField(default='a'),
            preserve_default=False,
        ),
    ]
