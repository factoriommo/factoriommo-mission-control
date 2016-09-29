# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_server_daemon_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionAmountStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
                ('server', models.ForeignKey(to='core.Server')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='productionstat',
            name='server',
        ),
        migrations.DeleteModel(
            name='ProductionStat',
        ),
    ]
