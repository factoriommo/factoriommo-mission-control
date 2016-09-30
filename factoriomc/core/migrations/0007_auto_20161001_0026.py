# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_server_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
