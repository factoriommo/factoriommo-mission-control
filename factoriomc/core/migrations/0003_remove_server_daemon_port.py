# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_server_auth_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='daemon_port',
        ),
    ]
